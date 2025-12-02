from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from web.db.db import get_db
from web.auth.auth import login_required

bpb = Blueprint('blog', __name__)

@bpb.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    print(posts)
    return render_template('blog/index.html', posts=posts)
