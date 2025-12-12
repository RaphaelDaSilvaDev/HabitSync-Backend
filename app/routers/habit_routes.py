from typing import Annotated

from fastapi import APIRouter, Query, Response, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.error_schema import ErrorResponse
from app.schemas.habit_schema import (
    HabitConclusionReturn,
    HabitConclusionUnmarkReturn,
    HabitCreate,
    HabitReturn,
    HabitUpdate,
)
from app.schemas.response import BaseResponse
from app.services.habit_service import HabitService
from app.utils.database import get_db
from app.utils.security import verify_token

habit_router = APIRouter(prefix='/habit', tags=['habit'])

Session = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(verify_token)]


@habit_router.post(
    '/create',
    response_model=BaseResponse[HabitReturn],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': BaseResponse[HabitReturn]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
    },
)
async def create_habit(
    data: HabitCreate,
    user: CurrentUser,
    db: Session,
):
    response = await HabitService.create_habit(data, user, db)
    return BaseResponse(
        status='success',
        message='Habit created successfully',
        data=response,
    )


@habit_router.get(
    '/',
    response_model=BaseResponse[list[HabitReturn]],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[list[HabitReturn]]},
    },
)
async def get_all_habit_by_user(user: CurrentUser, db: Session):
    response = await HabitService.get_habits_by_user_id(user, db)
    return BaseResponse(
        status='success',
        message='Get all habit for this user',
        data=response,
    )


@habit_router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def delete_habit_by_id(
    id: int,
    user: CurrentUser,
    db: Session,
):
    await HabitService.delet_habit(id, user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@habit_router.post(
    '/mark-done/{id}',
    response_model=BaseResponse[HabitConclusionReturn],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'model': BaseResponse[HabitConclusionReturn]
        },
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def mark_done(
    id: int,
    user: CurrentUser,
    db: Session,
):
    response = await HabitService.mark_conclusion(id, user, db)
    return BaseResponse(
        status='success',
        message='Habit marked done successfully',
        data=response,
    )


@habit_router.delete(
    '/unmark-done/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def unmark_done(
    id: int,
    user: CurrentUser,
    db: Session,
):
    await HabitService.unmark_conclusion(id, user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@habit_router.get(
    '/completed',
    response_model=BaseResponse[list[HabitReturn]],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BaseResponse[HabitConclusionUnmarkReturn]
        },
    },
)
async def get_habits_completed_by_day(
    user: CurrentUser,
    db: Session,
    date=Query(..., alias='date'),
):
    response = await HabitService.get_habits_completed_by_day(date, user, db)
    return BaseResponse(
        status='success',
        message=f'Habits completed in date {date}',
        data=response,
    )


@habit_router.get(
    '/upcoming',
    response_model=BaseResponse[list[HabitReturn]],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BaseResponse[HabitConclusionUnmarkReturn]
        },
    },
)
async def get_upcoming_habits(user: CurrentUser, db: Session):
    response = await HabitService.get_upcoming_habits(user, db)
    return BaseResponse(
        status='success', message='Habits upcoming today', data=response
    )


@habit_router.get(
    '/{id}',
    response_model=BaseResponse[HabitReturn],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[HabitReturn]},
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def get_habit_by_id(
    id: int,
    user: CurrentUser,
    db: Session,
):
    response = await HabitService.get_habit_by_id(id, user, db)
    return BaseResponse(
        status='success', message='Habit return successfully', data=response
    )


@habit_router.patch(
    '/{id}',
    response_model=BaseResponse[HabitReturn],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[HabitReturn]},
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def update_habit_by_id(
    id: int,
    data: HabitUpdate,
    user: CurrentUser,
    db: Session,
):
    response = await HabitService.update_habit_by_id(id, data, user, db)
    return BaseResponse(
        status='success',
        message='Habit updated successfully',
        data=response,
    )
