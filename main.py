import sqlite3

import jsonify as jsonify
from flask import Flask, request
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



# def get_rating(data_rating):
#     response = []
#     rating = data_rating.join(",")
#     query = f"SELECT title, rating, description FROM netflix WHERE  rating IN ({rating})"
#     result = db_connect('netflix.db, query')
#     for line in result:
#         line_dict = {
#             "title": line[0],
#             "rating": line1,
#             "description": line[2]
#         }
#         response.append(line_dict)
#     return response

@app.route('/movie/yea/')
def search_year():
    if request.nethod == 'GET':
        resource = []
        start_year = request.args.get('start_year')
        end_year = request.args.get('end_year')
        if start_year and end_year:
            query = f"""
            select title, release_year
            from netflix
            where release_year between {start_year} and {end_year}
            limit 100;
            """
            result = db_connect('netflix.db', query)

            print(result)

            for line in result:
                line_dict = {
                    "title": line[0],
                    "release_year": line[0],
                }
                response.append(line_dict)
            return  jsonify(response)

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


app.run (debug=True, port=8000)

