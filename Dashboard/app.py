from flask import Flask, render_template, redirect, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_table import Col, Table
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired
import xml.etree.ElementTree as ET

import os
import psycopg2


## Auxiliary functions
def all_reddit_sources():
    output = [("rc_2005_12", "rc_2005_12")]
    for year in range(2006, 2016):
        for month in range(1, 13):
            table_name = "rc_{0}_{1:02d}".format(year, month)
            output.append((table_name, table_name))
    for month in range(1, 12):
        table_name = "rc_2016_{0:02d}".format(month)
        output.append((table_name, table_name))
    return output

def all_se_domains():
    output = []
    tree = ET.parse('Sites.xml')
    root = tree.getroot()
    for child in root:
        output.append(child.attrib['Url'][8:].replace('.', '_'))
    return output

def all_se_sources():
    output = []
    doms = all_se_domains()
    for dom in doms:
        for data in ['Badges',
                     'Comments',
                     'PostHistory',
                     'PostLinks',
                     'Posts',
                     'Tags',
                     'Users',
                     'Votes']:
            source = "{}_{}_xml".format(dom, data)
            output.append((source, source))
    return output


## Config
app = Flask(__name__)
bootstrap = Bootstrap(app)

def set_db_config(user_var, pw_var, host_var, name_var):
    db_type = "postgresql://"
    db_user = os.environ[user_var]
    db_password = os.environ[pw_var]
    db_hostname = os.environ[host_var]
    db_name = os.environ[name_var]
    db_post = os.environ[port_var]
    app.config["SQLALCHEMY_DATABASE_URI"] = db_type + db_user + ":" + db_password +\
                                        "@" + db_hostname + ":" + db_port + "/" +\
                                        db_name

    
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = os.environ["FLASK_SECRET"]
                          
dict_user = os.environ['DICT_USER']
dict_pw = os.environ['DICT_PW']
dict_host = os.environ['DICT_HOST']
dict_port = os.environ['DICT_PORT']

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

class RedditForm(FlaskForm):
    table = SelectField("Raw Data", choices = all_reddit_sources())
    submit = SubmitField("Submit")

class SEForm(FlaskForm):
    table = SelectField("Raw Data", choices = all_se_sources())
    submit = SubmitField("Submit")



## Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalog")
def catalog():
    return render_template("catalog.html")


@app.route("/catalog/reddit", methods=["GET", "POST"])
def reddit():
    table = None
    form = RedditForm()
    if form.validate_on_submit():
        conn = psycopg2.connect("dbname='dictionaries' user='{}' host='{}' password='{}' port='{}'"
                                .format(dict_user, dict_pw, dict_host, dict_port))
        cur = conn.cursor()
        table_name = form.table.data
        cur.execute("""SELECT * from {}""".format(table_name))
        dict_rows = cur.fetchall()
        dict_dicts = map(lambda x: dict(variable=x[0], type=x[1], description=x[2]),
                         dict_rows)
        table = DictTable(dict_dicts)
    return render_template("reddit.html", form=form, table=table)

                          
@app.route("/catalog/stackexchange", methods=["GET", "POST"])
def stackexchange():
    table = None
    form = SEForm()
    if form.validate_on_submit():
        conn = psycopg2.connect("dbname='dictionaries' user='{}' host='{}' password='{}' port='{}'"
                                .format(dict_user, dict_pw, dict_host, dict_port))
        cur = conn.cursor()
        table_name = form.table.data
        cur.execute("""SELECT * from {}""".format(table_name))
        dict_rows = cur.fetchall()
        dict_dicts = map(lambda x: dict(variable=x[0], type=x[1], description=x[2]),
                         dict_rows)
        table = DictTable(dict_dicts)
    return render_template("stackexchange.html", form=form, table=table)


@app.route("/catalog/hackernews", methods=["GET", "POST"])
def hackernews():
    table = None
    return render_template("hackernews.html", form=form, table=table)


@app.route("/sample", methods=["GET", "POST"])
def sample():
    set_db_config("DB_USER", "DB_PASSWORD", "DB_HOSTNAME", "COMMENT_DB")
    table = None
    form = AppForm()
    if form.validate_on_submit():
        count_data = db.session \
                    .query(Comment.source, db.func.count(Comment.text)) \
                    .filter(Comment.datetime >= form.fromDate.data) \
                    .filter(Comment.datetime <= form.toDate.data) \
                    .group_by(Comment.source) \
                    .all()
        table = CommentTable(count_data)
    return render_template("sample.html", form=form, table=table)


## Models
class Comment(db.Model):
     __tablename__ = "long_comments"
     id = db.Column(db.Integer, primary_key=True)
     text = db.Column(db.String(64))
     datetime = db.Column(db.DateTime)
     source = db.Column(db.String(64))


## Tables
class CommentTable(Table):
    source = Col('Source')
    count = Col('Total')

class DictTable(Table):
    variable = Col("Variable")
    type = Col("Type")
    description = Col("Description")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
