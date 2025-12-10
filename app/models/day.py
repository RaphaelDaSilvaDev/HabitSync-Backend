from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.habit_day import habits_days
from app.utils.database import Base


class Day(Base):
    __tablename__ = 'days'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    habits: Mapped[list['Habit']] = relationship(  # noqa: F821
        secondary=habits_days, back_populates='frequency', lazy='selectin'
    )
    updated_at: Mapped[datetime] = mapped_column(default=func.now())
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    def __init__(self, name):
        self.name = name
