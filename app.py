import flask as flk
from flask import request,redirect
import numpy as np
import json
import os
import pandas as pd
from tf_idf_1 import TfIdfIndex
from data_manager import DataManager,read_csv
indexer = TfIdfIndex()
# import keras
# import keras.layers as layers
# import keras.models as models
# print(data5[['aired_str','aired_string']])
app = flk.Flask(__name__)
data_manager = read_csv('processed_data.csv')
@app.route("/")
def index():
    rows,_ = data_manager.get_rows_and_list_page_for_list(1)
    return flk.render_template("index.html",rows=rows)


@app.route("/AboutMe")
def aboutme():
    return flk.render_template("Aboutme.html")


@app.route("/film/<film_name>")
def anime_film(film_name):
    title,genres,episodes,year = data_manager.get_anime_info_by_name(film_name)
    return flk.render_template("anime-info.html",film_name=title,content="content",episodes=episodes,genres=genres,year=year)

    
@app.route("/category/<category_name>/<page>")
def anime_category(category_name,page):
    # sort to specific category
    rows,list_page = data_manager.get_rows_and_list_page_for_category(category_name,page)
    return flk.render_template("category_list.html",rows = rows, category_name=category_name,page=int(page),list_page = list_page)


@app.route("/list/<page>")
def anime_page(page):
    rows,list_page = data_manager.get_rows_and_list_page_for_list(page)
    return flk.render_template("category_list.html",page=int(page),rows=rows,list_page=list_page)


@app.route("/year/<year>/<page>")
def anime_year(year,page):
    rows,list_page= data_manager.get_rows_and_list_page_for_year(year,page)
    return flk.render_template("category_list.html",page=int(page),rows=rows,list_page=list_page)#,cat_name=year)

@app.route("/api/get_searched_list",methods=['post'])
def get_search_list():
    query = request.form['query']
    return flk.url_for('searched/1',query=query)


@app.route("/searched/<page>",methods=["post","get"])
def searched(page):
    query = request.args['query']
    print(query)
    p = int(page)
    searched = indexer.Retrieve(query)
    num_row= 8
    num_col=4
    x = []
    for i in searched:
        x.append(data[data['anime_id'] == i[0]].iloc[0])
    print(x)
    if x==[]:
        return flk.render_template('category_list.html',page=p,rows=[])
    x = pd.DataFrame(x)
    url_D = x[["image_url","title"]]
    rows = get_rows(url_D,num_row,num_col,p)

    return flk.render_template('category_list.html',page=p,rows=rows)


if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    
    # app.run()
# host='0.0.0.0'

