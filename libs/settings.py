from sqlalchemy import create_engine
import sqlalchemy as sa

rotten_engine = sa.create_engine('mssql://GUILHERME/rotten_tomatoes_top_movies?trusted_connection=yes&&driver=ODBC+Driver+17+for+SQL+Server')