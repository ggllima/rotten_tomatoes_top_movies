from __future__ import annotations
from typing import List
import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy_continuum import make_versioned

make_versioned(user_cls=None)

class Base(DeclarativeBase):
    pass

movies_genre = Table(
    "movies_genre",
    Base.metadata,
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
    Column("ranking_movie_id", ForeignKey("ranking_movie.id"), primary_key=True),
)

movies_director = Table(
    "movies_director",
    Base.metadata,
    Column("director_id", ForeignKey("director.id"), primary_key=True),
    Column("ranking_movie_id", ForeignKey("ranking_movie.id"), primary_key=True),
)

class Ranking_movie(Base):
    __tablename__ = 'ranking_movie'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title_id: Mapped[int] = mapped_column(ForeignKey("title.id"))
    title: Mapped["Title"] = relationship(back_populates="ranking_movie")
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))
    genre: Mapped["Genre"] = relationship(back_populates="ranking_movie")
    date_id: Mapped[int] = mapped_column(ForeignKey("date.id"))
    date: Mapped["Date"] = relationship(back_populates="ranking_movie")
    critic_score: Mapped[int] = mapped_column(Integer())
    people_score: Mapped[int] = mapped_column(Integer())
    total_reviews: Mapped[int] = mapped_column(Integer())
    total_ratings: Mapped[int] = mapped_column(Integer())
    box_office: Mapped[float] = mapped_column(Float())
    
    
    
class Title(Base):
    __tablename__ = "title"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title_movie: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["Ranking_movie"]] = relationship(back_populates="title")
    
class Language(Base):
    __tablename__ = "language"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    language_movie: Mapped[str] = mapped_column(String(30))
    ranking: Mapped[List["Ranking_movie"]] = relationship(back_populates="language")
    
    
class Genre(Base):
    __tablename__ = "genre"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    genre_movie: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["Ranking_movie"]] = relationship(back_populates="genre")
    
class Director(Base):
    __tablename__ = "director"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    director_movie: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["Ranking_movie"]] = relationship(back_populates="director")
    
    
class Date(Base):
    __tablename__ = "date"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nk_date: Mapped[int] = mapped_column(Integer())
    date_value: Mapped[Date] = mapped_column(Date())
    year: Mapped[int] = mapped_column(Integer())
    month: Mapped[int] = mapped_column(Integer())
    day: Mapped[int] = mapped_column(Integer())
    

    

    