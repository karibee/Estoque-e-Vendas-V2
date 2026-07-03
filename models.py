from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from database import Base

class Produto_orm(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    dono_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    preco: Mapped[float] = mapped_column(nullable=False)

    dono: Mapped["Usuario_orm"] = relationship(back_populates="produtos")

class Usuario_orm(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    login : Mapped[str] = mapped_column(unique=True, nullable=False)
    senha : Mapped[str] = mapped_column(nullable=False)

    produtos: Mapped["Produto_orm"] = relationship(back_populates="dono")