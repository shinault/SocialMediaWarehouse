from flask import Flask, render_template, redirect, session, url_for
from flask_bootstrap import Bootstrap
from flask_table import Col, Table
from flask_wtf import FlaskForm
import matplotlib.pyplot as plt
import pandas as pd
from wtforms import SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired
import xml.etree.ElementTree as ET

import base64
import io
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

def fill_feb(df):
    for day in range(30):
        date = '2012-02-{}'.format(day)
        if date not in df.Day:
            df.append({"Day": date, "Count": 0}, ignore_index=True)

def get_dict(table_name, dict_user, dict_host, dict_pw, dict_port):
    conn = psycopg2.connect("dbname='dictionaries' user='{}' host='{}' password='{}' port='{}'"
                            .format(dict_user, dict_host, dict_pw, dict_port))
    cur = conn.cursor()
    cur.execute("""SELECT * from {}""".format(table_name))
    dict_rows = cur.fetchall()
    cur.close()
    conn.close()
    dict_dicts = map(lambda x: dict(variable=x[0], type=x[1], description=x[2]),
                     dict_rows)
    return DictTable(dict_dicts)

def get_dict_simple(table_name, dict_user, dict_host, dict_pw, dict_port):
    conn = psycopg2.connect("dbname='dictionaries' user='{}' host='{}' password='{}' port='{}'"
                            .format(dict_user, dict_host, dict_pw, dict_port))
    cur = conn.cursor()
    cur.execute("""SELECT * from {}""".format(table_name))
    dict_rows = cur.fetchall()
    cur.close()
    conn.close()
    dict_dicts = map(lambda x: dict(variable=x[0], type=x[1]),
                     dict_rows)
    return DictSimple(dict_dicts)


# Technique from blog post technovechno.com
def make_plot(query_data):
    img = io.BytesIO()
    ## Create plot instructions
    df = pd.DataFrame(query_data, columns=["Source", "Day", "Count"])
    reddit = df.loc[df.Source=='reddit', ['Day','Count']]
    se = df.loc[df.Source=='stackexchange', ['Day','Count']]
    hn = df.loc[df.Source=='hackernews', ['Day','Count']]
    fill_feb(reddit)
    fill_feb(se)
    fill_feb(hn)    
    plt.plot('Day', 'Count', data=reddit, marker='', color='skyblue', linewidth=4, label="Reddit")
    plt.plot('Day', 'Count', data=se, marker='', color='olive', linewidth=4, label="Stack Exchange")
    plt.plot('Day', 'Count', data=hn, marker='', color='orange', linewidth=4, label="Hacker News")
    plt.xticks(rotation=90)
    plt.legend()
    
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

## Config
app = Flask(__name__)
bootstrap = Bootstrap(app)

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_hostname = os.environ['DB_HOSTNAME']
db_name = os.environ['DB_NAME']
db_port = os.environ['DB_PORT']
                          
dict_user = os.environ['DICT_USER']
dict_pw = os.environ['DICT_PW']
dict_host = os.environ['DICT_HOST']
dict_port = os.environ['DICT_PORT']

app.config["SECRET_KEY"] = os.environ["FLASK_SECRET"]


## Forms
class AppForm(FlaskForm):
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
    general_dictionary = get_dict('reddit', dict_user, dict_host, dict_pw, dict_port)
    if form.validate_on_submit():
        table = get_dict(form.table.data, dict_user, dict_host, dict_pw, dict_port)
    return render_template("reddit.html",
                           form=form,
                           table=table,
                           general_dictionary=general_dictionary)

                          
@app.route("/catalog/stackexchange", methods=["GET", "POST"])
def stackexchange():
    table = None
    form = SEForm()
    badges = get_dict_simple("se_badges", dict_user, dict_host, dict_pw, dict_port)
    comments = get_dict_simple("se_comments", dict_user, dict_host, dict_pw, dict_port)
    posthistory = get_dict_simple("se_posthistory", dict_user, dict_host, dict_pw, dict_port)
    postlinks = get_dict_simple("se_postlinks", dict_user, dict_host, dict_pw, dict_port)
    posts = get_dict_simple("se_posts", dict_user, dict_host, dict_pw, dict_port)
    tags = get_dict_simple("se_tags", dict_user, dict_host, dict_pw, dict_port)
    users = get_dict_simple("se_users", dict_user, dict_host, dict_pw, dict_port)
    votes = get_dict_simple("se_votes", dict_user, dict_host, dict_pw, dict_port)
    if form.validate_on_submit():
        table = get_dict(form.table.data, dict_user, dict_host, dict_pw, dict_port)
    return render_template("stackexchange.html",
                           form=form,
                           table=table,
                           badges=badges,
                           comments=comments,
                           posthistory=posthistory,
                           postlinks=postlinks,
                           posts=posts,
                           tags=tags,
                           users=users,
                           votes=votes)


@app.route("/catalog/hackernews", methods=["GET"])
def hackernews():
    conn = psycopg2.connect("dbname='dictionaries' user='{}' host='{}' password='{}' port='{}'"
                            .format(dict_user, dict_host, dict_pw, dict_port))
    cur = conn.cursor()
    table_name = "hackernews"
    cur.execute("""SELECT * from {}""".format(table_name))
    dict_rows = cur.fetchall()
    dict_dicts = map(lambda x: dict(variable=x[0], type=x[1], description=x[2]),
                     dict_rows)
    table = DictTable(dict_dicts)
    return render_template("hackernews.html", table=table)


@app.route("/sample", methods=["GET", "POST"])
def sample():
    graph = None
    form = AppForm()
    if form.validate_on_submit():
        conn = psycopg2.connect("dbname='comments' user='{}' host='{}' password='{}' port='{}'"
                                .format(dict_user, dict_host, dict_pw, dict_port))
        cur = conn.cursor()
        search_term = form.searchString.data
        select_statement = """SELECT source, DATE(datetime) AS day, COUNT(*) AS count FROM long_comments """
        where_clause = """WHERE (tsv @@ to_tsquery('%{}%')) GROUP BY source, day ORDER BY source, day"""
        cur.execute((select_statement + where_clause).format(search_term))
        count_rows = cur.fetchall()
        cur.close()
        conn.close()
        graph = make_plot(count_rows)
    return render_template("sample.html", form=form, graph=graph)


## Table Definitions
class DictTable(Table):
    variable = Col("Variable")
    type = Col("Type")
    description = Col("Description")
    
class DictSimple(Table):
    variable = Col("Variable")
    type = Col("Type")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)
