import flask as flk
from flask import request,redirect
import json
import os
from data_manager import DataManager,read_csv
# import keras
# import keras.layers as layers
# import keras.models as models
app = flk.Flask(__name__)
data_manager = read_csv('processed_data.csv')
@app.route("/")
def index():
    rows,_,ranked_list,random_list = data_manager.get_rows_and_list_page_for_list(1)
    return flk.render_template("index.html",rows=rows,ranked_list=ranked_list.to_dict('records'),random_list=random_list.to_dict('records'))


@app.route("/aboutme")
def aboutme():
    return flk.render_template("aboutme.html")


@app.route("/contact")
def contact():
    return flk.render_template("contact.html")


@app.route("/film/<film_name>")
def anime_film(film_name):
    title,genres,episodes,year,content,image_url = data_manager.get_anime_info_by_name(film_name)
    return flk.render_template("anime-info.html",film_name=title,content=content,episodes=episodes,genres=genres,year=year,image_url=image_url)

    
@app.route("/category/<category_name>/<page>")
def anime_category(category_name,page):
    # sort to specific category
    rows,list_page = data_manager.get_rows_and_list_page_for_category(category_name,page)
    return flk.render_template("category_list.html",rows = rows, category_name=category_name,page=int(page),list_page = list_page,cat_name="Category: {}".format(data_manager.get_category_name(category_name)),film_name='anime')

@app.route("/list/<page>")
def anime_page(page):
    rows,list_page,_,_ = data_manager.get_rows_and_list_page_for_list(page)
    return flk.render_template("category_list.html",page=int(page),rows=rows,list_page=list_page,cat_name="list of anime",film_name='anime')


@app.route("/year/<year>/<page>")
def anime_year(year,page):
    rows,list_page= data_manager.get_rows_and_list_page_for_year(year,page)
    return flk.render_template("category_list.html",page=int(page),rows=rows,list_page=list_page,cat_name="year:{}".format(year),film_name='anime')

@app.route("/api/get_searched_list",methods=['post'])
def get_search_list():
    query = request.form['query']
    return '/searched/1?query={}'.format(query)


@app.route("/searched/<page>",methods=["post","get"])
def searched(page):
    query = request.args['query']
    p = int(page)
    rows,list_page= data_manager.get_rows_for_searched_query(query,page)
    return flk.render_template('category_list.html',page=p,rows=rows,list_page=list_page,cat_name="Search for: {0}".format(query),film_name='anime')
@app.route("/film/<film_name>/<episode>")
def watch(film_name,episode):
    episodes = data_manager.get_epsiodes_from_name(film_name)
    return flk.render_template('anime-watching.html',episodes=int(episodes),episode=int(episode),film_name=film_name)
@app.route("/sitemap.xml")
def sitemap():
    f = open('./sitemap.xml')
    str = f.read()
    f.close()
    return str
if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    
    # app.run()
# host='0.0.0.0'

