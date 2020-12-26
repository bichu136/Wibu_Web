import flask as flk
import numpy as np
import json
import os
import pandas as pd
NEW_DOMAIN = "https://cdn.myanimelist.net/"


# import keras
# import keras.layers as layers
# import keras.models as models
data = pd.read_csv('./datasets/AnimeList.csv')
# data preprocessing
# change domain 
# for t in data['image_url'].values:
#      print(type(t))
def new_domain(str):
    r = ""
    if type(str)==type("str"):
        t = str.split('/')
        r = NEW_DOMAIN +t[-4] +'/'+t[-3] +'/'+t[-2] +'/'+t[-1]
    return r
new_img_url = pd.DataFrame({'image_url': [new_domain(t) for t in data['image_url'].values]})
data.update(new_img_url)

app = flk.Flask(__name__)
url_D = data[["image_url","title"]]
print(url_D[url_D.columns].iloc[0:4])
@app.route("/")
def index():
    print(data)
    num_row= 6
    
    rows = [[[url_D['title'].iloc[j+i*4],url_D['image_url'].iloc[j+i*4]] for j in range(4)] for i in range(num_row)]

    return flk.render_template("index.html",rows=rows)
@app.route("/AboutMe")
def aboutme():
    return flk.render_template("Aboutme.html")
@app.route("/film/<film_name>")
def anime_film(film_name):
    print(film_name)
    return flk.render_template("1anime.html",film_name=film_name)
@app.route("/category/<category_name>")
def anime_category(category_name):
    print(category_name)
    return flk.render_template("1cat.html",cat_name=category_name)
@app.route("/page/<page>")
def anime_page(page):
    print(page)
    return flk.render_template("1cat.html",page=page)
@app.route("/year/<year>")
def anime_year(year):
    print(year)
    return flk.render_template("1cat.html",cat_name=year)


if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    # app.run()
# host='0.0.0.0'

