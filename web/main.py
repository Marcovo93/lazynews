from pyexpat.errors import messages

from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True) # --> instance_relative_config=True --> serve per indicare la pagina fuori dalla cartella flaskr (da verificare)
#da verificare
app.config.from_mapping(
        SECRET_KEY='fox',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
@app.route("/")
def title():
    return render_template("home.html", title="Lazy News")

@app.route("/eventi")
def pagina_test():
    return render_template("eventi.html", title="Lazy News - Eventi")

@app.route("/contatti")
def contatti():
    return render_template("contatti.html", title="Lazy News - Contatti")


if __name__ == '__main__':
    app.run(debug=True)