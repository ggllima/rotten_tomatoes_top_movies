import pandas as pd
import sqlalchemy as sa


def create_foreing_key(df_fact:pd.core.frame.DataFrame, df_dimension:pd.core.frame.DataFrame, dimension_column:str, merge_method:str) -> pd.core.frame.DataFrame:
    df_merge = pd.merge(df_fact, df_dimension, how=merge_method, on=dimension_column)
    df_merge.rename(columns={'id_x':'id','id_y':dimension_column+'_id'},inplace=True)
    df_merge.drop(columns=[dimension_column],inplace=True)
    return df_merge


def send_data(data_frame:pd.core.frame.DataFrame, engine:sa.engine.base.Engine, table_name:str, schema:str, identity:bool=False) -> None:
    
    with engine.begin() as connection:
        if identity:
            connection.exec_driver_sql(f"SET IDENTITY_INSERT [{schema}].[{table_name}] ON")
        data_frame.to_sql(
            name=table_name,
            con=connection,
            schema=schema,
            if_exists='append',
            index=False,
        )
        if identity:
            connection.exec_driver_sql(f"SET IDENTITY_INSERT [{schema}].[{table_name}] OFF")