from datetime import date, datetime

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.api_exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from app.models.day import Day
from app.models.habit import Habit
from app.models.habit_conclution import HabitConclusion
from app.models.user import User
from app.schemas.habit_schema import (
    HabitConclusionReturn,
    HabitCreate,
    HabitReturn,
    HabitUpdate,
)


class HabitService:
    @staticmethod
    async def create_habit(
        data: HabitCreate, user: User, db: AsyncSession
    ) -> HabitReturn:
        existing_habit = await db.scalar(
            select(Habit).where(
                Habit.name == data.name, Habit.user_id == user.id
            )
        )

        if existing_habit:
            raise BadRequestException('This habit alreary exists')

        get_days = await db.scalars(
            select(Day).where(Day.id.in_(data.frequency))
        )

        days: list[Day] = get_days.all()

        habit = Habit(
            name=data.name,
            description=data.description,
            frequency=days,
            user_id=user.id,
        )

        db.add(habit)
        await db.commit()
        await db.refresh(habit)
        return HabitReturn(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            frequency=[day.name for day in habit.frequency],
        )

    @staticmethod
    async def get_habits_by_user_id(
        user: User, db: AsyncSession
    ) -> list[HabitReturn]:
        get_all_habits = await db.scalars(
            select(Habit).where(Habit.user_id == user.id)
        )

        all_habits = get_all_habits.all()

        formated_habits = [
            HabitReturn(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                frequency=[day.name for day in habit.frequency],
            )
            for habit in all_habits
        ]
        return formated_habits

    @staticmethod
    async def delet_habit(
        id: int, user: User, db: AsyncSession
    ) -> HabitReturn:
        existing_habit = await db.scalar(select(Habit).where(Habit.id == id))

        if not existing_habit:
            raise NotFoundException('Habit')

        if existing_habit.user_id != user.id and not user.is_admin:
            raise UnauthorizedException()

        await db.delete(existing_habit)
        await db.commit()

    @staticmethod
    async def mark_conclusion(
        id: int, user: User, db: AsyncSession
    ) -> HabitConclusionReturn:
        existing_habit = await db.scalar(
            select(Habit)
            .options(selectinload(Habit.frequency))
            .where(Habit.id == id)
        )

        if not existing_habit:
            raise NotFoundException('Habit')

        if existing_habit.user_id != user.id and not user.is_admin:
            raise UnauthorizedException()

        week_day = (datetime.now().weekday() + 1) % 7 + 1

        habit_days = [d.id for d in existing_habit.frequency]

        if week_day not in habit_days:
            raise ForbiddenException('This habit is not set for today')

        existing_conclusion = await db.scalar(
            select(HabitConclusion).where(
                HabitConclusion.habit_id == existing_habit.id,
                text('created_at::date = NOW()::date'),
            )
        )

        if existing_conclusion:
            raise ForbiddenException(
                'This habit has already been established today.'
            )

        conclusion = HabitConclusion(habit_id=existing_habit.id)

        db.add(conclusion)
        await db.commit()
        await db.refresh(conclusion)
        await db.refresh(existing_habit)

        return HabitConclusionReturn(
            id=conclusion.id,
            created_at=conclusion.created_at,
            habit=HabitReturn(
                id=existing_habit.id,
                name=existing_habit.name,
                description=existing_habit.description,
                frequency=[day.name for day in existing_habit.frequency],
            ),
        )

    @staticmethod
    async def unmark_conclusion(id: int, user: User, db: AsyncSession):
        existing_habit = await db.scalar(select(Habit).where(Habit.id == id))

        if not existing_habit:
            raise NotFoundException('Habit')

        if existing_habit.user_id != user.id and not user.is_admin:
            raise UnauthorizedException()

        existing_conclusion = await db.scalar(
            select(HabitConclusion).where(
                HabitConclusion.habit_id == existing_habit.id,
                text('created_at::date = NOW()::date'),
            )
        )

        if not existing_conclusion:
            raise ForbiddenException('This habit was not conclusion yet')

        await db.delete(existing_conclusion)
        await db.commit()

    @staticmethod
    async def get_habit_by_id(
        id: int, user: User, db: AsyncSession
    ) -> HabitReturn:
        existing_habit = await db.scalar(select(Habit).where(Habit.id == id))

        if not existing_habit:
            raise NotFoundException('Habit')

        if existing_habit.user_id != user.id and not user.is_admin:
            raise UnauthorizedException()

        return HabitReturn(
            id=existing_habit.id,
            name=existing_habit.name,
            description=existing_habit.description,
            frequency=[day.name for day in existing_habit.frequency],
        )

    @staticmethod
    async def update_habit_by_id(
        id: int, data: HabitUpdate, user: User, db: AsyncSession
    ) -> HabitReturn:
        existing_habit = await db.scalar(select(Habit).where(Habit.id == id))

        if not existing_habit:
            raise NotFoundException('Habit')

        if existing_habit.user_id != user.id and not user.is_admin:
            raise UnauthorizedException()

        existing_habit.name = data.name if data.name else existing_habit.name
        existing_habit.description = (
            data.description
            if data.description
            else existing_habit.description
        )

        if data.frequency:
            get_days = await db.scalars(
                select(Day).where(Day.id.in_(data.frequency))
            )
            days = get_days.all()
            existing_habit.frequency = days

        db.add(existing_habit)
        await db.commit()
        await db.refresh(existing_habit)

        return HabitReturn(
            id=existing_habit.id,
            name=existing_habit.name,
            description=existing_habit.description,
            frequency=[day.name for day in existing_habit.frequency],
        )

    @staticmethod
    async def get_habits_completed_by_day(
        date: date, user: User, db: AsyncSession
    ) -> list[HabitReturn]:
        get_habits_completed = await db.scalars(
            select(Habit, HabitConclusion)
            .options(selectinload(Habit.frequency))
            .join(Habit, Habit.id == HabitConclusion.habit_id)
            .where(
                text('date(habits_conclusion.created_at) = date(:date)'),
                Habit.user_id == user.id,
            )
            .params(date=date)
        )

        habits_completed = get_habits_completed.all()

        formated_habits = [
            HabitReturn(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                frequency=[day.name for day in habit.frequency],
            )
            for habit in habits_completed
        ]

        return formated_habits

    @staticmethod
    async def get_upcoming_habits(
        user: User, db: AsyncSession
    ) -> list[HabitReturn]:
        week_day = (datetime.now().weekday() + 1) % 7 + 1
        get_upcoming_habits = await db.scalars(
            select(Habit)
            .options(selectinload(Habit.frequency))
            .outerjoin(
                HabitConclusion,
                (HabitConclusion.habit_id == Habit.id)
                & (func.date(HabitConclusion.created_at) == func.date('now')),
            )
            .join(Habit.frequency)
            .where(
                Habit.user_id == user.id,
                HabitConclusion.id.is_(None),
                Day.id == week_day,
            )
        )

        upcoming_habits = get_upcoming_habits.all()

        formated_habits = [
            HabitReturn(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                frequency=[day.name for day in habit.frequency],
            )
            for habit in upcoming_habits
        ]

        return formated_habits
