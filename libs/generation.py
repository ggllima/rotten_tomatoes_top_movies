import pandas as pd
import numpy as np


def generation_df_movies(path) -> pd.core.frame.DataFrame:
    
    df_top_movies = pd.read_csv(path, sep=',')
    
    df_top_movies.drop(columns=['year','Unnamed: 0', 'synopsis', 'consensus', 'rating', 'writer', 'sound_mix', 'crew', 'link', 
                                'aspect_ratio', 'production_co', 'view_the_collection', 'producer', 'runtime','type'], inplace=True)
    
    df_top_movies.rename(columns={'release_date_(theaters)':'release_date_theaters', 'release_date_(streaming)':'release_date_streaming',
                                  'box_office_(gross_usa)':'box_office', 'original_language':'language'},inplace=True)
    
    df_top_movies['release_date_theaters'] = df_top_movies['release_date_theaters'].str.replace(' wide','',regex=True).replace(' limited','',regex=True).replace(',','', regex=True)
    df_top_movies['release_date_theaters'] = pd.to_datetime(df_top_movies['release_date_theaters'],format='%b %d %Y')
    df_top_movies = df_top_movies[(df_top_movies['box_office'].notna()) & (df_top_movies['release_date_theaters'] > '2000-01-01')].copy()
    
    df_top_movies.loc[df_top_movies['title'] == 'A Quiet Place', 'total_reviews'] = 384
    
    df_top_movies = df_top_movies.drop_duplicates(['title', 'critic_score', 'people_score', 'total_reviews',
           'total_ratings', 'genre', 'language', 'director',
           'release_date_theaters', 'release_date_streaming',
           'box_office']).reset_index(drop=True).copy()
    
    df_top_movies['release_date_theaters'] = df_top_movies['release_date_theaters'].fillna('1900-01-01')
    df_top_movies['release_date_streaming'] = df_top_movies['release_date_streaming'].fillna('1900-01-01')
    df_top_movies['people_score'] = df_top_movies['people_score'].fillna(0)
    
    df_top_movies['release_date_theaters'] = pd.to_datetime(df_top_movies['release_date_theaters'], format="%Y-%m-%d", errors="coerce")
    df_top_movies['release_date_streaming'] = pd.to_datetime(df_top_movies['release_date_streaming'], format="%b %d, %Y", errors="coerce")
    
    df_top_movies['box_office'] = np.where(df_top_movies['box_office'].str.contains('M') == True, df_top_movies['box_office']+'000.000',df_top_movies['box_office'])
    df_top_movies['box_office'] = np.where(df_top_movies['box_office'].str.contains('K') == True, df_top_movies['box_office']+'000',df_top_movies['box_office'])
    
    
    df_top_movies['total_ratings'] = df_top_movies['total_ratings'].str.replace('\D','',regex=True)
    df_top_movies['box_office'] = df_top_movies['box_office'].str.replace('[^0-9]+','',regex=True)
    
    df_top_movies['id'] = range(1,df_top_movies.index.stop + 1)
    

    # df_top_movies = df_top_movies[['id','title', 'language', 'critic_score', 'release_date_theaters', 'release_date_streaming' ,'people_score', 'total_reviews', 'total_ratings', 'box_office']]
    
    return df_top_movies
    
    
def dim_title(path) -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies(path)
    df_title = pd.DataFrame({'title':list(df_top_movies['title'].unique())})
    df_title['id'] = range(1,df_title.index.stop + 1)
    df_title = df_title[['id','title']]
    return df_title


def dim_genre(path) -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies(path)
    df_top_movies['genre'] = df_top_movies['genre'].str.split(',')
    df_genre = pd.DataFrame({'genre':df_top_movies[['genre']].explode("genre").reset_index(drop=True).copy()['genre'].str.strip().unique()})
    df_genre['id'] = range(1,df_genre.index.stop + 1)
    df_genre = df_genre[['id','genre']]
    return df_genre

def dim_language(path) -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies(path)
    df_language = pd.DataFrame({'language':list(df_top_movies['language'].unique())})
    df_language = df_language.fillna('Uninformed')
    df_language['id'] = range(1,df_language.index.stop + 1)
    df_language = df_language[['id','language']]
    return df_language


def dim_director(path) -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies(path)
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

    df['id'] = range(1,df.index.stop + 1)

    df = df[['id','nk_date', 'date_value', 'year', 'month', 'day']].copy()

    return df

def rel_movies_director(df_director, df_top_movies) -> pd.core.frame.DataFrame:
    
    dict_director = dict(zip(df_director['director'], df_director['id']))
    df_top_movies['director'] = df_top_movies['director'].str.split(',')
    df_top_moviesWdirector = df_top_movies[['id','director']].explode('director')
    df_top_moviesWdirector['director'] = df_top_moviesWdirector['director'].str.strip()
    df_top_moviesWdirector.replace({'director':dict_director},inplace=True)
    df_top_moviesWdirector.rename(columns={'director':'director_id'},inplace=True)
    return df_top_moviesWdirector

def rel_movies_genre(df_genre, df_top_movies) -> pd.core.frame.DataFrame:
    
    dict_genre = dict(zip(df_genre['genre'], df_genre['id']))
    df_top_movies['genre'] = df_top_movies['genre'].str.split(',')
    df_top_moviesWgenre = df_top_movies[['id','genre']].explode('genre')
    df_top_moviesWgenre['genre'] = df_top_moviesWgenre['genre'].str.strip()
    df_top_moviesWgenre.replace({'genre':dict_genre},inplace=True)
    df_top_moviesWgenre.rename(columns={'genre':'genre_id'},inplace=True)
    return df_top_moviesWgenre