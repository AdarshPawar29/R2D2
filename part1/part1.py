from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:r2d2dev@35.226.127.184/r2d2db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class moviedata(db.Model):
    __tablename__ = 'moviedata'
    id = db.Column(db.Integer, primary_key=True)
    moviename = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    starcast = db.Column(db.String(250), nullable=False)
    movieid = db.Column(db.String(250),  nullable=False)
    def __init__(self, moviename, rating, starcast, movieid):
        self.moviename = moviename
        self.rating = rating
        self.starcast = starcast
        self.movieid = movieid

class moviedataschema(ma.Schema):
    class Meta:
        fields = ('id', 'moviename', 'rating', 'starcast', 'movieid')

moviedata_schema = moviedataschema(many=True)

db.create_all()

@app.route("/autocomplete/<prefix>", methods=["GET"])
def autocomplete(prefix):
    movie_get = moviedata.query.filter(moviedata.moviename.like(prefix+'%')).limit(5)
    return moviedata_schema.jsonify(movie_get)

@app.route("/movieid/<movie>", methods=["GET"])
def movieid_detail(movie):
    movie_get = moviedata.query.filter(moviedata.movieid.like(movie))
    return moviedata_schema.jsonify(movie_get)

if __name__ == '__main__':
    app.run(debug=True)