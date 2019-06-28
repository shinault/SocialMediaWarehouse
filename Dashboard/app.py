from flask import Flask, render_template, redirect, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_table import Col, Table
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired

import os

## Config
app = Flask(__name__)
bootstrap = Bootstrap(app)

def set_db_config(user_var, pw_var, host_var, name_var):
    db_type = "postgres://"
    db_user = os.environ[user_var]
    db_password = os.environ[pw_var]
    db_hostname = os.environ[host_var]
    db_name = os.environ[name_var]
    app.config["SQLALCHEMY_DATABASE_URI"] = db_type + db_user + ":" + db_password +\
                                        "/" + db_hostname +  "/" + db_name

    
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = os.environ["FLASK_SECRET"]

## Forms
class AppForm(FlaskForm):
    fromDate = DateField("Initial date:",
                       format='%Y-%m-%d',
                       validators=[DataRequired()])
    toDate = DateField("Terminal date:",
                       format='%Y-%m-%d',
                       validators=[DataRequired()])
    searchString = StringField("Search comments for this term:")
    submit = SubmitField("Submit")

class CatalogForm(FlaskForm):
    data_src = SelectField("Data Source",
                           choices = [("reddit", "Reddit"),
                                      ("se", "Stack Exchange"),
                                      ("hn", "Hacker News")])
    submit = SubmitField("Submit")


## Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalog")
def catalog():
    return render_template("catalog.html")

@app.route("/catalog/dictionary", methods=["GET", "POST"])
def dictionary():
    set_db_config("DB_USER", "DB_PASSWORD", "DB_HOSTNAME", "CATALOG_DB")
    form = CatalogForm()
    return render_template("dictionary.html", form=form)

@app.route("/catalog/stats", methods=["GET", "POST"])
def stats():
    form = CatalogForm()
    return render_template("stats.html", form=form)

@app.route("/sample", methods=["GET", "POST"])
def sample():
    set_db_config("DB_USER", "DB_PASSWORD", "DB_HOSTNAME", "COMMENT_DB")
    table = None
    form = AppForm()
    if form.validate_on_submit():
        count_data = db.session \
                    .query(Comment.source, db.func.count(Comment.text)) \
                    .filter(Comment.timestamp >= form.fromDate.data) \
                    .filter(Comment.timestamp <= form.toDate.data) \
                    .group_by(Comment.source) \
                    .all()
        table = CommentTable(count_data)
    return render_template("sample.html", form=form, table=table)


## Models
class Comment(db.Model):
     __tablename__ = "long_comments"
     id = db.Column(db.Integer, primary_key=True)
     text = db.Column(db.String(64))
     timestamp = db.Column(db.DateTime)
     source = db.Column(db.String(64))


## Tables
class CommentTable(Table):
    source = Col('Source')
    count = Col('Total')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
