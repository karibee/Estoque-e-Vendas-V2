from sqlalchemy.orm import mapped_column, Mapped
from database import Base

class Produto_orm(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    preco: Mapped[float] = mapped_column ()