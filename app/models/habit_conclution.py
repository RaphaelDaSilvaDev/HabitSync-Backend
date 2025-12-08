from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.utils.database import Base


class HabitConclusion(Base):
    __tablename__ = 'habits_conclusion'

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    habit_id: Mapped[int] = mapped_column(ForeignKey('habits.id'))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    def __init__(self, habit_id):
        self.habit_id = habit_id
