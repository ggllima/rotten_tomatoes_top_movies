import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_continuum import make_versioned

make_versioned(user_cls=None)

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __versioned__ = {}
    __tablename__ = 'movie'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nk_movie: Mapped[str] = mapped_column(String(50))
    