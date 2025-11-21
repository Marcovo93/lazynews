import os
from auth.auth import bp
from db import db
from flask import Flask, render_template
from blog import bpb
from datetime import datetime


def create_app(test_config=None):
    # Crea app Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configurazione di default
    app.config.from_mapping(
        SECRET_KEY='fox',
        DATABASE=os.path.join(app.instance_path, 'lazynews.sqlite'),
    )
    app.debug = True

    # Crea la cartella Instance/ se non esiste
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Inizializza l'estensione DB
    db.init_app(app)


    #if not os.path.exists(app.config['DATABASE']):
    #    with app.app_context():
    #        db.init_db()
    #        print('Database creato con successo')
    #else:
    #    print('Database già esistente...')




    # importa e inizializza il modulo db QUI dentro, dopo aver creato app
    #registra iil Blueprint --> app.register_blueprint(bp)
    app.register_blueprint(bp)
    app.register_blueprint(bpb)
    app.add_url_rule('/', endpoint='index')


# ------- Variabili Global ------- #

    date_now = datetime.now()
    date_time_g = date_now.strftime("%d-%m-%Y %H:%M:%S")
    events_g = [
    {"settore": "mercato azionario", "campo": "crypto", "url": "mercato_azionario"},
    {"settore": "informatica", "campo": "sviluppo", "url": "informatica"},
    {"settore": "politica", "campo": "sotto sviluppo", "url": "politica"},
]

# ----------------------------------- #

    @app.route("/home")
    def home():
        return render_template("home.html", time=date_time_g)

    @app.route("/notizie")
    def notizie():
        return render_template("notizie.html", time=date_time_g, eventi=events_g)

    @app.route("/contatti")
    def contatti():
        return render_template("contatti.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/eventi/mercato_azionario/crypto")
    def mercato_azionario():
        return render_template("mercato_azionario.html", eventi=events_g)

    @app.route("/eventi/informatica/sviluppo")
    def informatica():
        return render_template("informatica.html", eventi=events_g)

    @app.route("/eventi/politica/sotto_sviluppo")
    def politica():
        return render_template("politica.html", eventi=events_g)

    return app

# entry point per "python web/main.py"
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
