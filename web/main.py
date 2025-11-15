from auth.auth import bp
from db import db
import os
from flask import Flask, render_template
from blog import bpb
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='fox',
        DATABASE=os.path.join(app.instance_path, 'lazynews.sqlite'),
    )
    app.debug = True

    with app.app_context():
        db.init_db()


    #if not os.path.exists(app.config['DATABASE']):
    #    with app.app_context():
    #        db.init_db()
    #        print('Database creato con successo')
    #else:
    #    print('Database già esistente...')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # importa e inizializza il modulo db QUI dentro, dopo aver creato app
    #registra iil Blueprint --> app.register_blueprint(bp)
    db.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(bpb)
    app.add_url_rule('/', endpoint='index')


    @app.route("/home")
    def home():
        date_now = datetime.now()
        date_time = date_now.strftime("%d-%m-%Y %H:%M:%S")
        return render_template("home.html", time=date_time)

    @app.route("/eventi")
    def eventi():
        date_now = datetime.now()
        date_time = date_now.strftime("%d-%m-%Y %H:%M:%S")
        return render_template("eventi.html", time=date_time)

    @app.route("/contatti")
    def contatti():
        return render_template("contatti.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    return app

# entry point per "python web/main.py"
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
