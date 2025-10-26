import sqlite3 #libreria sqlite3 utile per piccole app ad uso proprio
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.row
        return g.db

    def close_db(e=None):
        db = g.pop('db', None)

        if db is not None:
            db.close()