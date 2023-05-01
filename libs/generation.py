import pandas as pd
import numpy as np

def generation_df_movies(path='data/rotten_tomatoes_top_movies.csv') -> pd.core.frame.DataFrame:
    
    df_top_movies = pd.read_csv(path, sep=',')
    
    df_top_movies.drop(columns=['year','Unnamed: 0', 'synopsis', 'consensus', 'rating', 'writer', 'sound_mix', 'crew', 'link', 
                                'aspect_ratio', 'production_co', 'view_the_collection', 'producer', 'runtime','type'], inplace=True)
    
    df_top_movies.rename(columns={'release_date_(theaters)':'release_date_theaters', 'release_date_(streaming)':'release_date_streaming',
                                  'box_office_(gross_usa)':'box_office_gross_usa', 'original_language':'language_id', 'title':'title_id'},inplace=True)
    
    df_top_movies['release_date_theaters'] = df_top_movies['release_date_theaters'].str.replace(' wide','',regex=True).replace(' limited','',regex=True).replace(',','', regex=True)
    df_top_movies['release_date_theaters'] = pd.to_datetime(df_top_movies['release_date_theaters'],format='%b %d %Y')
    df_top_movies = df_top_movies[(df_top_movies['box_office_gross_usa'].notna()) & (df_top_movies['release_date_theaters'] > '2000-01-01')].copy()
    
    df_top_movies.loc[df_top_movies['title_id'] == 'A Quiet Place', 'total_reviews'] = 384
    
    df_top_movies = df_top_movies.drop_duplicates(['title_id', 'critic_score', 'people_score', 'total_reviews',
           'total_ratings', 'genre', 'language_id', 'director',
           'release_date_theaters', 'release_date_streaming',
           'box_office_gross_usa']).reset_index(drop=True).copy()
    
    df_top_movies['release_date_theaters'] = df_top_movies['release_date_theaters'].fillna('1900-01-01')
    df_top_movies['release_date_streaming'] = df_top_movies['release_date_streaming'].fillna('1900-01-01')
    
    df_top_movies['release_date_theaters'] = pd.to_datetime(df_top_movies['release_date_theaters'], format="%Y-%m-%d", errors="coerce")
    df_top_movies['release_date_streaming'] = pd.to_datetime(df_top_movies['release_date_streaming'], format="%b %d, %Y", errors="coerce")
    
    df_top_movies['box_office_gross_usa'] = np.where(df_top_movies['box_office_gross_usa'].str.contains('M') == True, df_top_movies['box_office_gross_usa']+'000.000',df_top_movies['box_office_gross_usa'])
    df_top_movies['box_office_gross_usa'] = np.where(df_top_movies['box_office_gross_usa'].str.contains('K') == True, df_top_movies['box_office_gross_usa']+'000',df_top_movies['box_office_gross_usa'])
    
    
    df_top_movies['total_ratings'] = df_top_movies['total_ratings'].str.replace('\D','',regex=True)
    df_top_movies['box_office_gross_usa'] = df_top_movies['box_office_gross_usa'].str.replace('[^0-9]+','',regex=True)

#     df_top_movies = df_top_movies[['title_id', 'language_id', 'date_id', 'critic_score', , 'people_score', 'total_reviews', 'total_ratings', 'release_date_theaters',
#                                    'release_date_streaming', 'box_office_gross_usa']]
    
    return df_top_movies
    
    
def dim_title() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    dim_title = pd.DataFrame({'title':list(df_top_movies['title'].unique())})
    dim_title = dim_title[['title']]
    return dim_title


def dim_genre() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_top_movies['genre'] = df_top_movies['genre'].str.split(',')
    df_genre = pd.DataFrame({'genre':df_top_movies[['genre']].explode("genre").reset_index(drop=True).copy()['genre'].str.strip().unique()})
    df_genre['id'] = range(1,df_genre.index.stop + 1)
    df_genre = df_genre[['id','genre']]
    return df_genre

def dim_language() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_language = pd.DataFrame({'language':list(df_top_movies['original_language'].unique())})
    df_language = df_language.fillna('Uninformed')
    return df_language


def dim_director() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_top_movies['director'] = df_top_movies['director'].str.split(',')
    df_director = pd.DataFrame({'director':df_top_movies[['director']].explode("director").reset_index(drop=True).copy()['director'].str.strip().unique()})
    df_director['id'] = range(1,df_director.index.stop + 1)
    df_director = df_director[['id','director']]
    return df_director


def dim_date(start_date:str, end_date:str) -> pd.core.frame.DataFrame:
    df = pd.DataFrame({"date_value": pd.date_range(start_date, end_date)})
    
    df_standart_value_nan = pd.DataFrame({"date_value": [pd.to_datetime('1900-01-01')]})

    df = pd.concat([df_standart_value_nan, df]).reset_index(drop=True)
    
    df["nk_date"] = df.date_value.dt.strftime('%Y-%m-%d').str.replace('-','').astype(int)
    df["year"] = df.date_value.dt.year
    df["month"] = df.date_value.dt.month
    df["day"] = df.date_value.dt.day

    df = df[['nk_date', 'date_value', 'year', 'month', 'day']].copy()

    return df

def rel_top_moviesWdirector() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_director = dim_director()
    dict_director = dict(zip(df_director['director'], df_director['id']))
    df_top_movies['director'] = df_top_movies['director'].str.split(',')
    df_top_moviesWdirector = df_top_movies[['id','director']].explode('director')
    df_top_moviesWdirector['director'] = df_top_moviesWdirector['director'].str.strip()
    df_top_moviesWdirector.replace({'director':dict_director},inplace=True)
    df_top_moviesWdirector.rename(columns={'director':'director_id'},inplace=True)
    return df_top_moviesWdirector

def rel_movies_genre() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_genre = dim_genre()
    dict_genre = dict(zip(df_genre['genre'], df_genre['id']))
    df_top_movies['genre'] = df_top_movies['genre'].str.split(',')
    df_top_moviesWgenre = df_top_movies[['id','genre']].explode('genre')
    df_top_moviesWgenre['genre'] = df_top_moviesWgenre['genre'].str.strip()
    df_top_moviesWgenre.replace({'genre':dict_genre},inplace=True)
    df_top_moviesWgenre.rename(columns={'genre':'genre_id'},inplace=True)
    return df_top_moviesWgenre