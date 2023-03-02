from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd
import os


def create_app(mode='dev'):
    # create the app
    app = Flask(__name__, instance_relative_config=True)

    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = os.environ.get('TWITTER_ANALYTICS_SECRET_KEY')

    if (app.config["SQLALCHEMY_DATABASE_URI"] is None) or (app.config["SQLALCHEMY_DATABASE_URI"] == ''):
        print("URL do Banco de Dados não encontrada.")
        exit(-1)

    if (app.secret_key is None) or (app.secret_key == ''):
        print("Chave Secreta não encontrada.")
        exit(-1)

    # create the Database extension
    db = SQLAlchemy()

    # initialize the app with the extension
    db.init_app(app)

    @app.route('/', methods=['POST', 'GET'])
    def home():

        if request.method == 'GET':
            return render_template('home.html')
        elif request.method == 'POST':
            return update()
        else:
            raise Exception("Erro ao processar a solicitação.")

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.errorhandler(Exception)
    def handle_exception(e):
        flash(str(e))
        return render_template('home.html')

    def update():
        if request.method == 'GET':
            raise Exception("Erro ao processar a consulta. Informações obrigatórias não encontradas.")

        tema = request.form['tema']

        # Log the request type
        app.logger.info("Consulta para o tema: {}".format(tema))

        if (tema is None) or (tema == ''):
            raise Exception("É necessário selecionar um item da lista!")

        sql = '''SELECT 
                 sum( (sentiment_label = 'positive')::int ) as qtd_positive ,
                 sum( (sentiment_label = 'negative')::int ) as qtd_negative,
                 sum( (sentiment_label = 'neutral')::int )  as qtd_neutral,
                 avg( (sentiment_label = 'positive')::int ) * 100 as percent_positive ,
                 avg( (sentiment_label = 'negative')::int ) * 100 as percent_negative,
                 avg( (sentiment_label = 'neutral')::int )  * 100 as percent_neutral,
                 date(tweet_created_at),
                 matching_rules_tag
                 FROM tweet_analytics 
                 WHERE matching_rules_tag = \'{}\'
                 GROUP by date(tweet_created_at), matching_rules_tag
                 ORDER by date
                '''

        df = pd.DataFrame(db.session.execute(text(sql.format(tema))).mappings().all())
        df.set_index('date', inplace=True)

        total = df[['qtd_positive', 'qtd_negative', 'qtd_neutral']].sum().sum()

        return render_template('result.html', result={'tema': tema,
                                                      'total': total,
                                                      'df': df})

    @app.route('/compare_all')
    def compare_all():

        sql = '''SELECT 
                 sum( (sentiment_label = 'positive')::int ) as qtd_positive ,
                 sum( (sentiment_label = 'negative')::int ) as qtd_negative,
                 sum( (sentiment_label = 'neutral')::int )  as qtd_neutral,
                 avg( (sentiment_label = 'positive')::int ) * 100 as percent_positive ,
                 avg( (sentiment_label = 'negative')::int ) * 100 as percent_negative,
                 avg( (sentiment_label = 'neutral')::int )  * 100 as percent_neutral,
                 date(tweet_created_at),
                 matching_rules_tag
                 FROM tweet_analytics 
                 WHERE matching_rules_tag in ('Economia', 'Educação', 'Imposto de Renda', 'Saúde', 'Segurança', 'Sistema Único de Saúde')
                 GROUP by date(tweet_created_at), matching_rules_tag
                 ORDER by date
                '''

        result = pd.DataFrame(db.session.execute(text(sql)).mappings().all())
        result.set_index('date', inplace=True)


        return render_template('compare_all.html', result=result)

    return app
