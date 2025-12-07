from sqlalchemy import Column, ForeignKey, Table

from app.utils.database import Base

habits_days = Table(
    "habits_days",
    Base.metadata,
    Column("habit_id", ForeignKey("habits.id"), primary_key=True),
    Column("day_id", ForeignKey("days.id"), primary_key=True),
)
