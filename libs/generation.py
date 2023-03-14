import pandas as pd

def generation_df_movies(path='../data/rotten_tomatoes_top_movies.csv') -> pd.core.frame.DataFrame:
    
    df_top_movies = pd.read_csv(path, sep=',')
    
    df_top_movies.drop(columns=['Unnamed: 0', 'synopsis', 'consensus', 'rating', 'writer', 'sound_mix', 'crew', 'link', 
                                'aspect_ratio', 'production_co', 'view_the_collection', 'producer', 'runtime','type'], inplace=True)
    
    df_top_movies.rename(columns={'release_date_(theaters)':'release_date_theaters'},inplace=True)
    
    df_top_movies['release_date_theaters'] = df_top_movies['release_date_theaters'].str.replace(' wide','',regex=True).replace(' limited','',regex=True).replace(',','', regex=True)
    df_top_movies['release_date_theaters'] = pd.to_datetime(df_top_movies['release_date_theaters'],format='%b %d %Y')
    df_top_movies = df_top_movies[(df_top_movies['box_office_(gross_usa)'].notna()) & (df_top_movies['release_date_theaters'] > '2000-01-01')].copy()
    
    df_top_movies.loc[df_top_movies['title'] == 'A Quiet Place', 'total_reviews'] = 384
    
    df_top_movies = df_top_movies.drop_duplicates(['title', 'year', 'critic_score', 'people_score', 'total_reviews',
           'total_ratings', 'genre', 'original_language', 'director',
           'release_date_theaters', 'release_date_(streaming)',
           'box_office_(gross_usa)']).reset_index(drop=True).copy()
    
    return df_top_movies


def dim_type() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    dim_type = pd.DataFrame({'type':list(df_top_movies['type'].unique())})
    dim_type['id'] = range(1, dim_type.index.stop+1)
    dim_type = dim_type[['id','type']]
    return dim_type
    
    
def dim_title() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    dim_title = pd.DataFrame({'title':list(df_top_movies['title'].unique())})
    dim_title['id'] = range(1, dim_title.index.stop+1)
    dim_title = dim_title[['id','title']]
    return dim_title


def dim_genre() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_top_movies['genre'] = df_top_movies['genre'].str.split(',')
    df_genre = pd.DataFrame({'genre':df_top_movies[['genre']].explode("genre").reset_index(drop=True).copy()['genre'].str.strip().unique()})
    df_genre['id'] = range(1,df_genre.index.stop + 1)
    df_genre = df_genre[['id','genre']]
    return df_genre


def df_top_moviesWgenre() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_genre = dim_genre()
    dict_genre = dict(zip(df_genre['genre'], df_genre['id']))
    df_top_moviesWgenre = df_top_movies[['id','genre']].explode('genre')
    df_top_moviesWgenre['genre'] = df_top_moviesWgenre['genre'].str.strip()
    df_top_moviesWgenre.replace({'genre':dict_genre},inplace=True)
    return df_top_moviesWgenre


def dim_language() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_language = pd.DataFrame({'original_language':list(df_top_movies['original_language'].unique())})
    df_language['id'] = range(1, df_language.index.stop+1)
    df_language = df_language[['id','original_language']]
    return df_language


def dim_director() -> pd.core.frame.DataFrame:
    
    df_top_movies = generation_df_movies()
    df_top_movies['director'] = df_top_movies['director'].str.split(',')
    df_director = pd.DataFrame({'director':df_top_movies[['director']].explode("director").reset_index(drop=True).copy()['director'].str.strip().unique()})
    df_director['id'] = range(1,df_director.index.stop + 1)
    df_director = df_director[['id','director']]
    return df_director