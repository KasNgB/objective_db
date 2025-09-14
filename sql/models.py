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


class Image(Base):
    __tablename__ = "images"

    image_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.current_timestamp(), nullable=False
    )

    analysis: Mapped["Analysis"] = relationship(
        back_populates="image",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,  # <- required when using delete-orphan in 1-1
        passive_deletes=True,  # <- trust DB ON DELETE CASCADE
    )

    __table_args__ = (
        CheckConstraint(
            "(width IS NULL OR width > 0) AND (height IS NULL OR height > 0)",
            name="ck_images_positive_dimensions",
        ),
    )


class Analysis(Base):
    __tablename__ = "analysis"

    image_ID: Mapped[int] = mapped_column(
        ForeignKey("images.image_ID", ondelete="CASCADE"),
        primary_key=True,
    )
    exposure: Mapped[float | None] = mapped_column(Float)
    dominant_color: Mapped[str | None] = mapped_column(String(7))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.current_timestamp(), nullable=False
    )

    image: Mapped[Image] = relationship(back_populates="analysis")
