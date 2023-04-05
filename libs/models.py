from __future__ import annotations
from typing import List
import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from libs import settings as st

rotten_engine = sa.create_engine('mssql://GUILHERME/rotten_tomatoes_top_movies?trusted_connection=yes&&driver=ODBC+Driver+17+for+SQL+Server')
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

class RankingMovie(Base):
    __tablename__ = 'ranking_movie'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title_id: Mapped[int] = mapped_column(ForeignKey("title.id"))
    title: Mapped["DimTitle"] = relationship(back_populates="ranking_movie")
    # genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))
    # genre: Mapped["DimGenre"] = relationship(back_populates="ranking_movie")
    # director_id: Mapped[int] = mapped_column(ForeignKey("director.id"))
    # director: Mapped["DimDirector"] = relationship(back_populates="ranking_movie")
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"))
    language: Mapped["DimLanguage"] = relationship(back_populates="ranking_movie")
    date_id: Mapped[int] = mapped_column(ForeignKey("date.id"))
    date: Mapped["DimDate"] = relationship(back_populates="ranking_movie")
    critic_score: Mapped[int] = mapped_column(Integer())
    people_score: Mapped[int] = mapped_column(Integer())
    total_reviews: Mapped[int] = mapped_column(Integer())
    total_ratings: Mapped[int] = mapped_column(Integer())
    box_office: Mapped[float] = mapped_column(Float())
    
    
    
class DimTitle(Base):
    __tablename__ = "title"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title_movie: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["RankingMovie"]] = relationship(back_populates="title")
    
class DimLanguage(Base):
    __tablename__ = "language"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    language_movie: Mapped[str] = mapped_column(String(30))
    ranking: Mapped[List["RankingMovie"]] = relationship(back_populates="language")
    
    
class DimGenre(Base):
    __tablename__ = "genre"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    genre_movie: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["RankingMovie"]] = relationship(back_populates="genre")
    
class DimDirector(Base):
    __tablename__ = "director"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    director_movie: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["RankingMovie"]] = relationship(back_populates="director")
    
    
class DimDate(Base):
    __tablename__ = "date"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nk_date: Mapped[int] = mapped_column(Integer())
    date_value: Mapped[Date] = mapped_column(Date())
    year: Mapped[int] = mapped_column(Integer())
    month: Mapped[int] = mapped_column(Integer())
    day: Mapped[int] = mapped_column(Integer())
    
    



