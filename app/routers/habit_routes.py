from datetime import date

from fastapi import APIRouter, Query, Response, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

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
from app.utils.auth_login import verify_token
from app.utils.database import get_db

habit_router = APIRouter(prefix='/habit', tags=['habit'])


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
    user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    created_habit = HabitService.create_habit(data, user, db)
    return BaseResponse(
        status='success',
        message='Habit created successfully',
        data=created_habit,
    )


@habit_router.get(
    '/',
    response_model=BaseResponse[list[HabitReturn]],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[list[HabitReturn]]},
    },
)
async def get_all_habit_by_user(
    user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    all_habits = HabitService.get_habits_by_user_id(user, db)
    return BaseResponse(
        status='success',
        message='Get all habit for this user',
        data=all_habits,
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
    id: int, user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    HabitService.delet_habit(id, user, db)
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
    id: int, user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    habit = HabitService.mark_conclusion(id, user, db)
    return BaseResponse(
        status='success', message='Habit marked done successfully', data=habit
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
    id: int, user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    HabitService.unmark_conclusion(id, user, db)
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
    date: date = Query(..., alias='date'),
    user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    completed_habits = HabitService.get_habits_completed_by_day(date, user, db)
    return BaseResponse(
        status='success',
        message=f'Habits completed in date {date}',
        data=completed_habits,
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
async def get_upcoming_habits(
    user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    upcoming_habits = HabitService.get_upcoming_habits(user, db)
    return BaseResponse(
        status='success', message='Habits upcoming today', data=upcoming_habits
    )


@habit_router.get(
    '/{id}',
    response_model=BaseResponse[HabitReturn],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BaseResponse[HabitConclusionUnmarkReturn]
        },
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def get_habit_by_id(
    id: int, user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    habit = HabitService.get_habit_by_id(id, user, db)
    return BaseResponse(
        status='success', message='Habit return successfully', data=habit
    )


@habit_router.patch(
    '/{id}',
    response_model=BaseResponse[HabitReturn],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': BaseResponse[HabitConclusionUnmarkReturn]
        },
        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def update_habit_by_id(
    id: int,
    data: HabitUpdate,
    user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    updated_habit = HabitService.update_habit_by_id(id, data, user, db)
    return BaseResponse(
        status='success',
        message='Habit updated successfully',
        data=updated_habit,
    )
