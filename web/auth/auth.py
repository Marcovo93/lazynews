import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from web.db.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


#decoratore per pagina di registrazione
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email richiesto'
        elif not username:
            error = 'Username richiesto'
        elif not password:
            error = 'Password richiesta'

        if error is None:
            try:
                hashed_password = generate_password_hash(password, method='pbkdf2')
                db.execute(
                    'INSERT INTO users (email, username, password) VALUES (?, ?, ?)',
                    (email, username, hashed_password),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Utente {username} già registrato."
            else:
                return redirect(url_for("auth.login"))

                flash(error)

    return render_template('register.html') #('auth/register.html')

@bp.route('/register2', methods=('GET', 'POST'))
def register2():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        data_nascita = request.form['data']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not nome:
            error = 'Nome obbligatorio'
        elif not cognome:
            error = 'Cognome obbligatorio'
        elif not data_nascita:
            error = 'Data di nascita obbligatoria'
        elif not email:
            error = 'Email obbligatoria'
        elif not password:
            error = 'Password richiesta'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO users2 (nome, cognome, data_nascita, email, password) VALUES (?, ?, ?, ?, ?)',
                    (nome, cognome, data_nascita, email, password),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Email {email} già registrata"
            else: redirect(url_for("auth.login2"))

    return render_template('register2.html')

@bp.route("/login2")
def login2():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = get_db().execute(
            'SELECT * FROM users2 WHERE email = ?', (email,)
        ).fetchone()
    return render_template("login_2.html")

#decoratore per pagina di login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        print(user)
        if user is None:
            error = 'Username errato.'
            #elif not check_password_hash(user['password'], password):
            #error = 'Password errata'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)

    return render_template('login.html')

#caricare utente loggato
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index)'))

#login required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/sqlite')
def select_table():
    db = get_db()
    table_sqlite = db.execute(
        'SELECT * FROM users'
    ).fetchall()
    return render_template('sqlite.html', utenti=table_sqlite)