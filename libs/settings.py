import sqlalchemy as sa
import pandas as pd
conn_rotten_engine = sa.create_engine('mssql://GUILHERME/rotten_tomatoes_top_movies?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
