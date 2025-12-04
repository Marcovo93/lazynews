import os, requests
from web.auth.auth import bp
from web.db import db
from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from web.blog import bpb
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


    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            db.init_db()
            print('Database creato con successo')
    else:
        print('Database già esistente...')




    # importa e inizializza il modulo db QUI dentro, dopo aver creato app
    #registra iil Blueprint --> app.register_blueprint(bp)
    app.register_blueprint(bp)
    app.register_blueprint(bpb)
    app.add_url_rule('/', endpoint='index')


# ------- Variabili Global ------- #

    # newsapi ----- #
    api_key = "514e79afc1a24dc6aa19297d49f50bb4"
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    filtered = data.get("articles", [])
    result = []

    for n in filtered:
        result.append({
            "author": n.get("author"),
            "content": n.get("content"),
            "description": n.get("description"),
            "published": n.get("publishedAt"),
            "id": n.get("source", {}).get("id"),
            "name": n.get("name"),
            "title": n.get("title"),
            "url": n.get("url"),
            "urlimg": n.get("urlToImage")
        })
    # --------- #

    date_now = datetime.now()
    date_time_g = date_now.strftime("%d-%m-%Y %H:%M:%S")
    owners_g = [
        {"name_owner": "Marco", "surname_owner": "Volpe", "email": "MarcoV@Lazynews.com", "image": "static/img/dev.jpg"},
        {"name_owner": "Fabio", "surname_owner": "Volpe", "email": "FabioV@Lazynews.com", "image": "static/img/dev.jpg"}
    ]
    # ------- API route ------- #

    @app.route("/home")
    def home():
        return render_template("home.html", result=result)

    # ----------------------------------- #

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
