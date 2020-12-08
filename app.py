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

if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
    # app.run()
# host='0.0.0.0'

