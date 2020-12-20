import flask as flk
import numpy as np
import json
import os
# import keras
# import keras.layers as layers
# import keras.models as models
app = flk.Flask(__name__)
@app.route("/")
def index():
    return flk.render_template("index.html")
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


if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    # app.run()
# host='0.0.0.0'

