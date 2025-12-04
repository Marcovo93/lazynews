import functools, requests, os
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify
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

    # ------- API route ------- #
    # get JSON

# Users management APIs
# POST /api/users/update - download users and update DB - return { total_users: X }, 200
@bp.route("/api/users/update", methods=['POST'])
def download_update_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    data = response.json()
    db = get_db()
    row_count = 0

    for users in data:
        db.execute(
            'INSERT INTO api_news (username, email, name, city, street, company, company_description) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (users["username"], users["email"], users["name"], users["address"]["city"], users["address"]["street"], users["company"]["name"], users["company"]["bs"],)
        )
        row_count += 1
    db.commit()

    response_data = {
        "message": f"Insert completed. Total row {row_count}",
        "status": "success"
    }
    return jsonify(data, response_data), 201



# GET  /api/users - return all users info, 200
@bp.route("/api/users", methods=['GET'])
def return_all_users():
    db = get_db()
    users = db.execute('SELECT * FROM api_news').fetchall()
    users_list = [dict(row) for row in users]
    count_users = len(users)

    if not users:
        return jsonify("message:" " No users found"), 404

    return jsonify(users_list,
                   "status:" " ok",
                   "message:" f" Number of users {count_users}"
                   ), 200

# GET  /api/users/<id> - return user's info, 200
@bp.route("/api/users/<int:id>", methods=['GET'])
def return_id_users_info(id):
    db = get_db()
    select = db.execute('SELECT * FROM api_news WHERE id = ?', (id,))
    user_info = select.fetchone()

    if user_info is None:
        return jsonify("error: " "user not found"), 404

    user_data = dict(user_info)

    return jsonify(user_data), 200

# POST /api/users - params: name, etc - return user's info, 201


# PUT  /api/users/<id> - udpate user's info - return new user's info, 200
@bp.route("/api/user/<int:id>", methods=['PUT'])
def update_user(id):
    db = get_db()
    put = {
        "username": "marcovo93",
        "email": "marcovolpe93@gmail.com",
    }

    db.execute(f'UPDATE api_news SET username = ?, email = ? WHERE id = {id}',
    (put["username"], put["email"])
    )
    db.commit()
    select = db.execute(f'SELECT * FROM api_news WHERE id = {id}',)
    user_info = select.fetchone()
    user_list = dict(user_info)

    response = {
        "status": "ok",
        "message": "put completed"
    }

    return jsonify(response, user_list), 200


# DELETE /api/users/<id> - delete user - return empty body, 200
@bp.route("/api/users/<int:id>", methods=['DELETE'])
def delete_user(id):
    db = get_db()
    db.execute(f'DELETE FROM api_news WHERE id = {id}',)
    db.commit()

    return "", 204


#@bp.route("/api/users/<id>", methods=['GET'])
#def api_get_user_by_id(id):
#    pass

@bp.route("/api/country")
def api_get_country():
    url = "https://restcountries.com/v3.1/name/italy"
    response = requests.get(url)
    data = response.json()
    filtered = []

    for country in data:
        filtered.append({
            "country_code": country["altSpellings"][0],
            "name_republic": country["altSpellings"][2],
            "capital": country["capital"],
            "car_side": country["car"]["side"],
            "continents": country["continents"],
            "currencies": country["currencies"]["EUR"]["name"],
            "population": country["population"]
        })

    return render_template("testAPI.html", filtered=filtered)

@bp.route("/news_test", methods=['GET'])
def getnewsapi():
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
            "name": n.get("name")
        })
    return render_template("notizie_dynamic.html", result=result) #return jsonify(result), 200

@bp.route("/api2", methods=['GET'])
def testapi():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    data = response.json()
    filtered = []

    for f in data:
        filtered.append({
            "address": f["address"]["city"]
        })

    return jsonify(filtered), 200


    # post JSON
#@bp.route("/api/users-jo", methods=['POST'])
#def api_add_users():
#    users = []
#    data = requests.get_json()
#    users.append(data)
#    return jsonify(data), 200
        # ----------------------------------- #

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