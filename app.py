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

#only get TV 
data6 = data5[data5["type"]=="TV"]
data7 = data6[data6["episodes"]>=10]
data7.update(data7['genre'].fillna('_'))
genres = []
for _,i in data7['genre'].iteritems():
    for j in i.split(','):
        if j.strip() not in genres:
            genres.append(j.strip())
for genre in genres:
    encoding = [genre in i for i in data7.genre]
    data7.insert(0,"genre_"+genre,encoding,True)
data7.drop(['genre'], axis=1, inplace=True)
print(data7.columns)
# print(data8.columns)

# aired_string process
date_time_aired = pd.DataFrame({'aired_str':[i.split('to')[0] for i in data7['aired_string']]})
data7.insert(0,"aired_str",pd.to_datetime(date_time_aired['aired_str']).to_list(),True)
#sort value
data7 = data7.sort_values(by='aired_str',ascending=False)

# print(data5[['aired_str','aired_string']])
app = flk.Flask(__name__)

@app.route("/")
def index():
    url_D = data7[["image_url","title"]]
    num_row= 6
    num_col=4
    rows = [[[url_D['title'].iloc[num_row*num_col*(1-1)+j+i*num_col],url_D['image_url'].iloc[num_row*num_col*(1-1)+j+i*num_col]] for j in range(num_col)] for i in range(num_row)]
    return flk.render_template("index.html",rows=rows)
@app.route("/AboutMe")
def aboutme():
    return flk.render_template("Aboutme.html")
@app.route("/film/<film_name>")
def anime_film(film_name):
    print(film_name)
    return flk.render_template("anime-info.html",film_name=film_name)
@app.route("/category/<category_name>/<page>")
def anime_category(category_name,page):
    
    #map the category
    # sort to specific category
    data8 = data7[data7["genre_"+category_name]==1]
    num_row= 8
    num_col=4
    p = int(page)
    url_D = data8[["image_url","title"]]
    rows = [[[url_D['title'].iloc[num_row*num_col*(p-1)+j+i*num_col],url_D['image_url'].iloc[num_row*num_col*(p-1)+j+i*num_col]] for j in range(num_col)] for i in range(num_row)]
    return flk.render_template("category_list.html",row = rows, category_name=category_name)
@app.route("/list/<page>")
def anime_page(page):
    num_row= 8
    num_col=4
    p = int(page)
    url_D = data7[["image_url","title"]]
    rows = [[[url_D['title'].iloc[num_row*num_col*(p-1)+j+i*num_col],url_D['image_url'].iloc[num_row*num_col*(p-1)+j+i*num_col]] for j in range(num_col)] for i in range(num_row)]
    return flk.render_template("category_list.html",page=page,rows=rows)
@app.route("/year/<year>")
def anime_year(year):
    print(year)
    return flk.render_template("category_list.html",cat_name=year)


if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    # app.run()
# host='0.0.0.0'

