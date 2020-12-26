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

#remove date Not available
data1 = data[data['aired_string']!='Not available']
# remove film that not airing 
data2 = data1[data1['aired']!="{'from': None, 'to': None}"]
# remove score <=3
data3 = data2[data2['score']>=3]
# remove favorites =0
data4 = data3[data3['favorites']!=0]
data4['rank'].fillna(0);
data5 = data4[data4['rank']>0]
# change domain 
def new_domain(str):
    r = ""
    if type(str)==type("str"):
        t = str.split('/')
        r = NEW_DOMAIN +t[-4] +'/'+t[-3] +'/'+t[-2] +'/'+t[-1]
    return r
new_img_url = pd.DataFrame({'image_url': [new_domain(t) for t in data['image_url'].values]})
data5.update(new_img_url)



# aired_string process
date_time_aired = pd.DataFrame({'aired_str':[i.split('to')[0] for i in data5['aired_string']]})
data5.insert(0,"aired_str",pd.to_datetime(date_time_aired['aired_str']).to_list(),True)
#sort value
data5 = data5.sort_values(by='aired_str',ascending=False)
print(data5[['aired_str','aired_string']])
app = flk.Flask(__name__)
url_D = data5[["image_url","title"]]
@app.route("/")
def index():
    print(url_D['image_url'])
    print(url_D['title'])
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

