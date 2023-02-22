from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd
import os


def create_app(mode='dev'):
    # create the extension
    db = SQLAlchemy()

    # create the app
    app = Flask(__name__, instance_relative_config=True)

    # configure the SQLite database, relative to the app instance folder
    # app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://thiagomf:bq9E5ExCwj7Xb@postgres-minha-nuvem-db.minhanuvem.org:8081/tweet_analytics'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # initialize the app with the extension
    db.init_app(app)

    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = b'RLRTq)glQA#E=n+QQ%RLC4eFC`"bleqq}yO24ds+`^3zTtv^I$jEFkKU>?:`uC#'

    # override default config values from config.py file located in "instance" folder
    is_file_configured = app.config.from_pyfile('config.py', silent=True)

    if not is_file_configured:
        # set default config vaules
        app.config.from_mapping()

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/update')
    def update():

        sql = '''SELECT tweet_id, sentiment_label, tweet_created_at, matching_rules_tag FROM tweet_analytics'''

        results = db.session.execute(text(sql))

        df = pd.DataFrame(results.mappings().all())

        df.set_index('tweet_created_at', inplace=True)

        df2 = df.query('matching_rules_tag=="Sistema Único de Saúde"').resample('h')['sentiment_label'].value_counts(
            normalize=True).unstack('sentiment_label')[['positive', 'neutral', 'negative']]

        print(df2)

        return render_template('result.html', df_result = df2)

    @app.errorhandler(Exception)
    def handle_exception(e):
        flash(str(e))
        return render_template('home.html')

    return app
