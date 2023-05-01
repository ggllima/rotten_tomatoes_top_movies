from __future__ import annotations
from typing import List
import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from libs import settings as st


class Base(DeclarativeBase):
    pass

rel_movies_genre = Table(
    "rel_movies_genre",
    Base.metadata,
    Column("genre_id", ForeignKey("dim_genre.id"), primary_key=True),
    Column("ranking_movie_id", ForeignKey("fact_ranking_movie.id"), primary_key=True),
)

rel_movies_director = Table(
    "rel_movies_director",
    Base.metadata,
    Column("director_id", ForeignKey("dim_director.id"), primary_key=True),
    Column("ranking_movie_id", ForeignKey("fact_ranking_movie.id"), primary_key=True),
)

class FactRankingMovie(Base):
    __tablename__ = 'fact_ranking_movie'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title_id: Mapped[int] = mapped_column(ForeignKey("dim_title.id"))
    title: Mapped["DimTitle"] = relationship(back_populates="fact_ranking_movie")
    # genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))
    # genre: Mapped["DimGenre"] = relationship(back_populates="fact_ranking_movie")
    # director_id: Mapped[int] = mapped_column(ForeignKey("director.id"))
    # director: Mapped["DimDirector"] = relationship(back_populates="fact_ranking_movie")
    language_id: Mapped[int] = mapped_column(ForeignKey("dim_language.id"))
    language: Mapped["DimLanguage"] = relationship(back_populates="fact_ranking_movie")
    date_id: Mapped[int] = mapped_column(ForeignKey("dim_date.id"))
    date: Mapped["DimDate"] = relationship(back_populates="fact_ranking_movie")
    critic_score: Mapped[int] = mapped_column(Integer())
    people_score: Mapped[int] = mapped_column(Integer())
    total_reviews: Mapped[int] = mapped_column(Integer())
    total_ratings: Mapped[int] = mapped_column(Integer())
    box_office: Mapped[float] = mapped_column(Float())
    
    
    
class DimTitle(Base):
    __tablename__ = "dim_title"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    ranking: Mapped[List["FactRankingMovie"]] = relationship(back_populates="dim_title")
    
class DimLanguage(Base):
    __tablename__ = "dim_language"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[str] = mapped_column(String(30))
    ranking: Mapped[List["FactRankingMovie"]] = relationship(back_populates="dim_language")
    
    
class DimGenre(Base):
    __tablename__ = "dim_genre"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["FactRankingMovie"]] = relationship(back_populates="dim_genre")
    
class DimDirector(Base):
    __tablename__ = "dim_director"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    director: Mapped[str] = mapped_column(String(50))
    ranking: Mapped[List["FactRankingMovie"]] = relationship(back_populates="dim_director")
    
    
class DimDate(Base):
    __tablename__ = "dim_date"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nk_date: Mapped[int] = mapped_column(Integer())
    date_value: Mapped[Date] = mapped_column(Date())
    year: Mapped[int] = mapped_column(Integer())
    month: Mapped[int] = mapped_column(Integer())
    day: Mapped[int] = mapped_column(Integer())
    ranking: Mapped[List["FactRankingMovie"]] = relationship(back_populates="dim_date")
    


    
    



