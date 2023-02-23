from flask import Flask, render_template, flash, request
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
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

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

    @app.route('/update', methods=['POST'])
    def update():

        if request.method == 'POST':
            sql = '''SELECT tweet_id, sentiment_label, tweet_created_at, matching_rules_tag FROM tweet_analytics where matching_rules_tag=\'{}\''''

            tema = request.form['tema']

            print("tema: {}".format(tema))

            if (tema is None) or (tema == ''):
                raise Exception("É necessário selecionar um item da lista!")

            results = db.session.execute(text(sql.format(tema)))

            df = pd.DataFrame(results.mappings().all())

            df_total_quantities = pd.DataFrame(df['sentiment_label'].value_counts()).sort_index(
                ascending=False).reset_index().rename({'index': 'sentiment', 'sentiment_label': 'value'}, axis=1)

            df_total_percentages = pd.DataFrame(df['sentiment_label'].value_counts(normalize=True)).sort_index(
                ascending=False).reset_index().rename({'index': 'sentiment', 'sentiment_label': 'value'}, axis=1)

            df.set_index('tweet_created_at', inplace=True)
            df_time_series = df.resample('h')['sentiment_label'].value_counts(normalize=True).unstack('sentiment_label')[['positive', 'neutral', 'negative']]

            df_sentiment_quantities = df.resample('h')['sentiment_label'].value_counts().unstack('sentiment_label')[['positive', 'neutral', 'negative']]

        return render_template('result.html', tema=tema,
                               df_time_series=df_time_series,
                               df_sentiment_quantities=df_sentiment_quantities,
                               df_total_quantities=df_total_quantities,
                               df_total_percentages=df_total_percentages)

    @app.errorhandler(Exception)
    def handle_exception(e):
        flash(str(e))
        return render_template('home.html')

    return app
