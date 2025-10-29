# web/main.py
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from auth.auth import bp
from web.db.db import get_db
import os
from flask import Flask, render_template, redirect




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='fox',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # importa e inizializza il modulo db QUI dentro, dopo aver creato app
    from db import db
    db.init_app(app)
    app.register_blueprint(bp)
    # registra le route (puoi anche importarle da un altro file se preferisci)
    @app.route("/")
    def home():
        return render_template("home.html", title="Lazy News")

    @app.route("/eventi")
    def eventi():
        return render_template("eventi.html", title="Lazy News - Eventi")

    @app.route("/contatti")
    def contatti():
        return render_template("contatti.html", title="Lazy News - Contatti")

    @app.route("/register")
    def registrazione():
        return render_template("register.html",)

    return app

# entry point per "python web/main.py"
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
