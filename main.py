import sqlite3

from collections import Counter

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def db_connect(db,query):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result

@app.route("/movie/title")
def search_title():
    if request.method == 'GET':
        responce = {}
        title = request.args.get('title')
        if title:
            query = f"""
                SELECT
                title,
                country,
                listed_in,
                release_year,
                description
                FROM netflix
                WHERE title = '{title}'
                ORDER BY release_year DESC
                LIMIT 1
            """
            result = db_connect('netflix.db', query)
            if len(result):
                responce = {
                    "title" : result[0][0],
                    "country" : result[0][0],
                    "listed_in" : result[0][0],
                    "release_year" : result[0][0],
                    "description" : result[0][0],
                }
        return jsonify(responce)


@app.route("/movie/year/")
def search_year():
    if request.method == 'GET':
        responce = []
        start_year = request.args.get('start_year')
        end_year = request.args.get('end_year')
        if start_year and end_year:
            query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {start_year} AND {end_year}
            LIMIT 100;
            """
            result = db_connect('netflix.db', query)
            for line in result:
                line_dict = {
                    "title": line[0],
                    "release_year": line[1],
                }
                responce.append(line_dict)
    return  jsonify(responce)


def get_rating(rating):
    responce = []
    if len(rating) > 1:
        str_rating = "','".join(rating)
    else:
        str_rating = "".join(rating)

    query = f""" SELECT title, description
                FROM netflix
                WHERE rating in ('{str_rating}')
                LIMIT 100"""
    result = db_connect('netflix.db', query)
    for line in result:
        line_dict = {
            "title": line[0],
            "rating": line[1],
            "description": line[2],
        }
        responce.append(line_dict)
    return responce


@app.route("/rating/children/")
def rating_children():
    rating = get_rating(['G'])
    return jsonify(rating)

@app.route("/rating/family/")
def rating_family():
    rating = get_rating(['PG','PG13'])
    return jsonify(rating)

@app.route("/rating/adult/")
def rating_adult():
    rating = get_rating(['R', 'NC-17'])
    return jsonify(rating)


@app.route("/genre/<genre>")
def search_genre(genre):
    query = f"""SELECT title, description
            FROM netflix
            WHERE listed_in like '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10"""
    result = db_connect('netflix.db', query)
    responce = []
    for line in result:
        line_dict ={
            "title": line[0],
            "description": line[1],
        }
        responce.append(line_dict)
    return jsonify(responce)

def search_pair (actor1, actor2):
    query = f"""SELECT [cast]
                FROM netflix
                WHERE [cast] LIKE '%{actor1}%' AND [cast] LIKE '%{actor2}%'"""
    result = db_connect('netflix.db', query)
    result_list = []
    for line in result:
        line_list = line[0].split(',')
        result_list += line_list
    counter = Counter(result_list)
    actors_list = []
    for key, value in counter.items():
        if value > 2 and key.strip() not in [actor1, actor2]:
            actors_list.append(key)
    return actors_list

def search(type_, release_year, listed_in):
    query = f"""SELECT title, description
                FROM netflix
                WHERE type = '{type_}' AND release_year = '{release_year}' AND listed_in LIKE '%{listed_in}%'
                """
    result = db_connect('netflix.db', query)
    responce = []
    for line in result:
        line_dict = {
            "title": line[0],
            "description": line[1],
        }
        responce.append(line_dict)
    return  json.dumps(responce)


print(search('Movie', '2016', 'comedies'))

app.run ()

