from sqlalchemy import create_engine, MetaData
import os

if __name__ == '__main__':
    conn = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if conn is not None and conn != '':
        engine = create_engine(conn)
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=engine)
        for table in metadata_obj.sorted_tables:
             print(table)