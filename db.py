from flask import current_app, g
import psycopg2
import os


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(host='postgres-minha-nuvem-db.minhanuvem.org:8081',
                                database='TWITTER_ANALYTICS_DB_NAME',
                                user=os.environ['TWITTER_ANALYTICS_DB_USERNAME'],
                                password=os.environ['TWITTER_ANALYTICS_DB_PASSWORD'])

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
