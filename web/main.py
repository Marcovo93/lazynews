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
    owners_g = [
        {"name_owner": "Marco", "surname_owner": "Volpe", "email": "MarcoV@Lazynews.com", "image": "static/img/dev.jpg"},
        {"name_owner": "Fabio", "surname_owner": "Volpe", "email": "FabioV@Lazynews.com", "image": "static/img/dev.jpg"}
    ]
    events_g = [
        {"settore": "Mercato azionario", "campo": "crypto", "url": "mercato_azionario"},
        {"settore": "Informatica", "campo": "sviluppo", "url": "informatica"},
        {"settore": "Politica", "campo": "sotto sviluppo", "url": "politica"},
    ]

    cronaca_g = [
        {"titolo": "Bitcoin supera nuovamente quota 100.000$ dopo una settimana volatile", "corpo": "Il prezzo di Bitcoin è tornato sopra la soglia psicologica dei 100k grazie a un incremento degli acquisti istituzionali. Gli analisti vedono segnali positivi, ma rimane alta la volatilità nel breve periodo."},
        {"titolo": "Apple rilascia aggiornamento di sicurezza urgente per macOS", "corpo": "Apple ha pubblicato una patch che corregge una vulnerabilità zero-day individuata da ricercatori indipendenti. L’azienda invita tutti gli utenti ad aggiornare immediatamente per evitare possibili exploit da parte di malware."},
        {"titolo": "Governo approva nuovo piano per il lavoro giovanile", "corpo": "Il Consiglio dei ministri ha varato un pacchetto di incentivi destinato alle imprese che assumono under 30 con contratti stabili. Le misure includono sgravi contributivi per 24 mesi e un fondo dedicato alla formazione digitale."}
    ]
# ----------------------------------- #

    @app.route("/home")
    def home():
        return render_template("home.html", time=date_time_g, eventi=events_g)

    @app.route("/notizie")
    def notizie():
        return render_template("notizie.html", time=date_time_g, eventi=events_g)

    @app.route("/about")
    def about():
        return render_template("about.html", owners=owners_g, reference="Example@lazynews.org")


        # ------- route dynamic ------- #

    @app.route("/eventi/<int:parametro>")
    def events_dynamic(parametro):
        evento_int = events_g[parametro]
        cronaca_int = cronaca_g[parametro]
        return render_template("notizie_dynamic.html", parametro=parametro, eventi=evento_int, cronaca=cronaca_int)

        # ----------------------------------- #

    return app



# entry point per "python web/main.py"
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
