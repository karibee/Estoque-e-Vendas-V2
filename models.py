from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from database import Base
from datetime import date

class Product_orm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    owner: Mapped["User_orm"] = relationship(back_populates="products")

class User_orm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    products: Mapped["Product_orm"] = relationship(back_populates="owner")
    profile: Mapped["Profile_orm"] = relationship(back_populates="owner", uselist=False)

class Profile_orm(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    cpf: Mapped[int] = mapped_column(unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(unique=True, nullable=True)
    birth_date: Mapped[date] = mapped_column(nullable=False)

    owner: Mapped["User_orm"] = relationship(back_populates="profile")
