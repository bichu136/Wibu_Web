import flask as flk
from flask import request,redirect
import numpy as np
import json
import os
import pandas as pd
from tf_idf_1 import TfIdfIndex
indexer = TfIdfIndex()
# import keras
# import keras.layers as layers
# import keras.models as models
def get_genres(x):
    return []
def get_rows(url_D,num_row,num_col,p):
    return [
        [
        [
        url_D['title'].iloc[num_row*num_col*(p-1)+j+i*num_col],
        url_D['image_url'].iloc[num_row*num_col*(p-1)+j+i*num_col]
        ] 
        for j in range(num_col) if num_row*num_col*(p-1)+j+i*num_col < len(url_D)
        ] 
        for i in range(num_row) 
        ]
data = pd.read_csv('processed_data.csv')
mapper = open('mapping_category.txt').readlines()
mapper = {i.strip().split('|')[0]: i.strip().split('|')[1] for i in mapper}
#sort value
data = data.sort_values(by='aired_str',ascending=False)

# print(data5[['aired_str','aired_string']])
app = flk.Flask(__name__)

@app.route("/")
def index():
    url_D = data[["image_url","title"]]
    num_row= 6
    num_col=4
    rows = get_rows(url_D,num_row,num_col,p=1)
    return flk.render_template("index.html",rows=rows)
@app.route("/AboutMe")
def aboutme():
    return flk.render_template("Aboutme.html")
@app.route("/film/<film_name>")
def anime_film(film_name):
    print(film_name)
    x = data[data['title']==film_name].iloc[0]
    title =  x['title']
    genres = get_genres(x)
    episodes = x['episodes']
    content = x['content']
    return flk.render_template("anime-info.html",film_name=title)
@app.route("/category/<category_name>/<page>")
def anime_category(category_name,page):
    # sort to specific category
    data8 = data[data["genre_"+mapper[category_name]]==True]
    num_row= 8
    num_col=4
    p = int(page)
    url_D = data8[["image_url","title"]]
    print(data8)
    print(url_D)
    rows = get_rows(url_D,num_row,num_col,p)
    return flk.render_template("category_list.html",rows = rows, category_name=category_name)

@app.route("/list/<page>")
def anime_page(page):
    num_row= 8
    num_col=4
    p = int(page)
    url_D = data[["image_url","title"]]
    rows = get_rows(url_D,num_row,num_col,p)
    return flk.render_template("category_list.html",page=page,rows=rows)
@app.route("/year/<year>")
def anime_year(year):
    print(year)
    return flk.render_template("category_list.html",cat_name=year)
@app.route("/api/get_searched_list",methods=['post'])
def get_search_list():
    query = request.form['query']
    return flk.url_for('searched',query=query,page='1')
@app.route("/searched",methods=["post","get"])
def searched():
    query = request.args['query']
    print(query)
    p = int(request.args['page'])
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
    print(x.columns)
    
    url_D = x[["image_url","title"]]
    rows = get_rows(url_D,num_row,num_col,p)
    return flk.render_template('category_list.html',page=p,rows=rows)
if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    
    # app.run()
# host='0.0.0.0'

