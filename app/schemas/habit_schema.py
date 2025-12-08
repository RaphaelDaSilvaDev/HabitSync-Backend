from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = ''
    frequency: list[int]


class HabitReturn(BaseModel):
    id: int
    name: str
    description: str
    frequency: list[str]

    model_config = {'from_attributes': True}


class HabitConclusionReturn(BaseModel):
    id: int
    habit: HabitReturn
    created_at: datetime

    model_config = {'from_attributes': True}


class HabitConclusionUnmarkReturn(BaseModel):
    id: int
    habit_id: int
    habit: str


class HabitUpdate(BaseModel):
    name: Optional[str] = ''
    description: Optional[str] = ''
    frequency: Optional[list[int]] = []
