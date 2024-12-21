import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    input_filename = params.input_filename
    database_user = params.database_user
    database_pwd = params.database_pwd
    database_host = params.database_host
    database_db = params.database_db
    database_port = params.database_port
    url = params.url
    # filename = 'yellow_tripdata_2021-01.csv'
    df_name = "_".join(input_filename.split("_")[:2])
    
    os.system(f"wget {url}")

    os.system(f"gzip -d {input_filename}")

    df = pd.read_csv(input_filename, nrows=1000, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])

    engine = create_engine(f'postgresql://{database_user}:{database_pwd}@{database_host}:{database_port}/{database_db}')

    df_iter = pd.read_csv(input_filename, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], iterator=True, chunksize=100000)

    df = next(df_iter)

    df.head(n=0).to_sql(name=df_name, con=engine, if_exists='replace')

    df.to_sql(name=df_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)

        df.to_sql(name=df_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')
    parser.add_argument('--input_filename')# = 'yellow_tripdata_2021-01.csv'
    parser.add_argument('--database_user')# = 'root'
    parser.add_argument('--database_pwd')# = 'root'
    parser.add_argument('--database_host')# = 'localhost'
    parser.add_argument('--database_db')# = 'ny_taxi'
    parser.add_argument('--database_port')# = 5432
    parser.add_argument('--url')# = 5432

    args = parser.parse_args()

    main(args)

