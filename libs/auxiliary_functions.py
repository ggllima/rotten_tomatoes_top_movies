import pandas as pd

def create_foreing_key(fact_df:pd.core.frame.DataFrame, dimension_df:pd.core.frame.DataFrame, dimension_column:str, merge_method:str) -> pd.core.frame.DataFrame:
    df_merge = pd.merge(fact_df, dimension_df, how=merge_method, on=dimension_column)
    df_merge.rename(columns={'id_x':'id','id_y':dimension_column+'_id'},inplace=True)
    df_merge.drop(columns=[dimension_column],inplace=True)
    return df_merge