import psycopg2
from sqlalchemy import create_engine, MetaData
import os


if __name__ == '__main__':
    # print(os.environ.get('TWITTER_ANALYTICS_DB_URL'))
    engine = create_engine('postgresql+psycopg2://thiagomf:bq9E5ExCwj7Xb@postgres-minha-nuvem-db.minhanuvem.org:8081/tweet_analytics')

    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    for table in metadata_obj.sorted_tables:
         print(table)