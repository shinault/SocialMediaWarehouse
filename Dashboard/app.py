from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

## Config
app = Flask(__name__)
bootstrap = Bootstrap(app)


## Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalog")
def catalog():
    return render_template("catalog.html")

@app.route("/sample")
def sample():
    return render_template("sample.html")
