from datetime import date, datetime

from fastapi import status
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.exceptions.api_exception import APIException
from app.models.day import Day
from app.models.habit import Habit
from app.models.habit_conclution import HabitConclusion
from app.models.user import User
from app.schemas.habit_schema import (
    HabitConclusionReturn,
    HabitConclusionUnmarkReturn,
    HabitCreate,
    HabitReturn,
    HabitUpdate,
)


class HabitService:
    @staticmethod
    def create_habit(data: HabitCreate, user: User, db: Session) -> HabitReturn:
        existing_habit = db.query(Habit).filter(Habit.name == data.name).first()

        if existing_habit:
            raise APIException(
                message="This habit alreary exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        days = db.query(Day).filter(Day.id.in_(data.frequency)).all()

        habit = Habit(
            name=data.name,
            description=data.description,
            frequency=days,
            user_id=user.id,
        )

        db.add(habit)
        db.commit()
        db.refresh(habit)
        return HabitReturn(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            frequency=[day.name for day in habit.frequency],
        )

    @staticmethod
    def get_habits_by_user_id(user: User, db: Session) -> list[HabitReturn]:
        all_habits = db.query(Habit).filter(Habit.user_id == user.id).all()

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
    def delet_habit(id: int, user: User, db: Session) -> HabitReturn:
        existing_habit = db.query(Habit).filter(Habit.id == id).first()

        if not existing_habit:
            raise APIException(
                message="Habit not found", status_code=status.HTTP_404_NOT_FOUND
            )

        if existing_habit.user_id != user.id and not user.is_admin:
            raise APIException(
                message="You don't have permission to delete this habit",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        db.delete(existing_habit)
        db.commit()
        return HabitReturn(
            id=existing_habit.id,
            name=existing_habit.name,
            description=existing_habit.description,
            frequency=[day.name for day in existing_habit.frequency],
        )

    @staticmethod
    def mark_conclusion(id: int, user: User, db: Session) -> HabitConclusionReturn:
        existing_habit = db.query(Habit).filter(Habit.id == id).first()

        if not existing_habit:
            raise APIException(
                message="This habit not exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if existing_habit.user_id != user.id and not user.is_admin:
            raise APIException(
                message="You don't have permission to delete this habit",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        week_day = (datetime.now().weekday() + 1) % 7 + 1

        habit_days = [d.id for d in existing_habit.frequency]

        if week_day not in habit_days:
            raise APIException(
                message="This habit not set for today",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        existing_conclusion = (
            db.query(HabitConclusion)
            .filter(
                HabitConclusion.habit_id == existing_habit.id,
                text("date(created_at, 'localtime') = date('now','localtime')"),
            )
            .first()
        )

        if existing_conclusion:
            raise APIException(
                message="This habit alreary marked today",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        conclusion = HabitConclusion(habit_id=existing_habit.id)

        db.add(conclusion)
        db.commit()

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
    def unmark_conclusion(
        id: int, user: User, db: Session
    ) -> HabitConclusionUnmarkReturn:
        existing_habit = db.query(Habit).filter(Habit.id == id).first()

        if not existing_habit:
            raise APIException(
                message="This habit not exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if existing_habit.user_id != user.id and not user.is_admin:
            raise APIException(
                message="You don't have permission to delete this habit",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        existing_conclusion = (
            db.query(HabitConclusion)
            .filter(
                HabitConclusion.habit_id == existing_habit.id,
                text("date(created_at, 'localtime') = date('now','localtime')"),
            )
            .first()
        )

        if not existing_conclusion:
            raise APIException(
                message="This habit was not conclusion yet",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        db.delete(existing_conclusion)
        db.commit()
        return HabitConclusionUnmarkReturn(
            id=existing_conclusion.id,
            habit_id=existing_habit.id,
            habit=existing_habit.name,
        )

    @staticmethod
    def get_habit_by_id(id: int, user: User, db: Session) -> HabitReturn:
        existing_habit = db.query(Habit).filter(Habit.id == id).first()

        if not existing_habit:
            raise APIException(
                message="Habit not found", status_code=status.HTTP_404_NOT_FOUND
            )

        if existing_habit.user_id != user.id and not user.is_admin:
            raise APIException(
                message="You don't have permission to delete this habit",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return HabitReturn(
            id=existing_habit.id,
            name=existing_habit.name,
            description=existing_habit.description,
            frequency=[day.name for day in existing_habit.frequency],
        )

    @staticmethod
    def update_habit_by_id(
        id: int, data: HabitUpdate, user: User, db: Session
    ) -> HabitReturn:
        existing_habit = db.query(Habit).filter(Habit.id == id).first()

        if not existing_habit:
            raise APIException(
                message="Habit not found", status_code=status.HTTP_404_NOT_FOUND
            )

        if existing_habit.user_id != user.id and not user.is_admin:
            raise APIException(
                message="You don't have permission to delete this habit",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        existing_habit.name = data.name if data.name else existing_habit.name
        existing_habit.description = (
            data.description if data.description else existing_habit.description
        )

        if data.frequency:
            days = db.query(Day).filter(Day.id.in_(data.frequency)).all()
            existing_habit.frequency = days

        db.add(existing_habit)
        db.commit()
        db.refresh(existing_habit)

        return HabitReturn(
            id=existing_habit.id,
            name=existing_habit.name,
            description=existing_habit.description,
            frequency=[day.name for day in existing_habit.frequency],
        )

    @staticmethod
    def get_habits_completed_by_day(
        date: date, user: User, db: Session
    ) -> list[HabitReturn]:
        habits_completed = (
            db.query(Habit, HabitConclusion)
            .join(Habit, Habit.id == HabitConclusion.habit_id)
            .filter(
                text("date(habits_conclusion_created_at) = date(:date)"),
                Habit.user_id == user.id,
            )
            .params(date=date)
            .all()
        )

        formated_habits = [
            HabitReturn(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                frequency=[day.name for day in habit.frequency],
            )
            for habit, _ in habits_completed
        ]

        return formated_habits

    @staticmethod
    def get_upcoming_habits(user: User, db: Session) -> list[HabitReturn]:
        week_day = (datetime.now().weekday() + 1) % 7 + 1
        upcoming_habits = (
            db.query(Habit)
            .outerjoin(
                HabitConclusion,
                (HabitConclusion.habit_id == Habit.id)
                & (func.date(HabitConclusion.created_at) == func.date("now")),
            )
            .join(Habit.frequency)
            .filter(
                Habit.user_id == user.id, HabitConclusion.id == None, Day.id == week_day
            )
        ).all()

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
