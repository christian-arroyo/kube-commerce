from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from apps.checkout_api.core.config import config


# Make database connection and session available to the rest of the application
engine = create_engine(config.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Checkout(Base):
    __tablename__ = "checkout"

    checkout_id: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(nullable=False)
    tax: Mapped[Decimal] = mapped_column(nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(nullable=False)
    total: Mapped[Decimal] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(nullable=False)
