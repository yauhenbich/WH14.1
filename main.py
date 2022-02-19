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
    print(result)
    con.close()
    return result

@app.route('/movie/title')
def search_title():
    # return 'test'
    if request.nethod == 'GET':
        resource = {}
        title = request.args.get('title')
        if title:
            query = f"""
            select
                title,
                country,
                listed_in,
                release_year,
                description
            from netflix
            where title = '{title}'
            order by release_year DESC
            LIMIT 1
            """
            result = db_connect('netflix.db', query)
        if len(result):
                response = {
                    "title" : result[0][0],
                    "country" : result[0][0],
                    "listed_in" : result[0][0],
                    "release_year" : result[0][0],
                    "description" : result[0][0],
                }
        return jsonify(response)


@app.route('/movie/yea/')
def search_year():
    if request.nethod == 'GET':
        resource = []
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
                    "release_year": line[0],
                }
                response.append(line_dict)
            return  jsonify(response)


def get_raling(rating):
    response = []
    if len(rating)>1:
        str_rating = "','".join(rating)
    else:
        str_rating = "".join(rating)
    print(str_rating)
    query = f""" SELECT 'title', 'country', 'release_year', 'listed_in', 'description', 'rating'
                FROM netflix
                WHERE rating in ('{str_rating}')
                LIMIT 100"""
    result = db_connect('netflix.db', query)
    for line in result:
        line_dict = {
            "title": line[0],
            "rating": line[1],
            "description": line[2]
        }
        response.append(line_dict)
    return response


@app.route('/rating/children/')
def rating_children():
    response = get_rating(['G'])
    return jsonify(response)

@app.route('/rating/family/')
def rating_family():
    response = get_rating(['PG','PG13'])
    return jsonify(response)

@app.route('/rating/adult/')
def rating_adult():
    response = get_rating(['R', 'NC-17'])
    return jsonify(response)


@app.route('/genre/<genre>')
def search_genre(genre):
    query = f"""SELECT title, description FROM netflix
            WHERE listed_in like "%{genre}%"
            ORDER BY relea_year DESC
            LIMIT 10"""
    result = db_connect('netflix.db', query)
    response = []
    for line in result:
        line_dict ={
            "title": line[0],
            "description": line[1]
        }
        response.append(line_dict)
    return jsonify(response)

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
    query = f"""SELECT title, DESCRIPTION
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

app.run (debug=True, port=8000)

