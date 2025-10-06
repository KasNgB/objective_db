from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    CheckConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Runs(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detected: Mapped[int | None] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(String, nullable=False)
    end_time: Mapped[datetime] = mapped_column(String, nullable=False)
