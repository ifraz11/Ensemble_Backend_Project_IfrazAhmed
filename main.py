#Ensemble Backend Project by I Ahmed

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initialize App

backend_app = Flask(__name__)
base_directory = os.path.abspath(os.path.dirname(__file__))

#Database
backend_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_directory, 'db.sqlite')
#backend_app['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(backend_app)

#initialize Marshmallow
ma = Marshmallow(backend_app)

# Movie Class (Object Creation)
class Movie(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    movie_title = db.Column(db.String(100), unique=True) #we dont want 2 movies with same name so unique = true
    description = db.Column(db.String(400))
    release_year = db.Column(db.Integer)
    duration = db.Column(db.Integer) #duration in minutes
    rating = db.Column(db.Float)
    likes = db.Column(db.Integer) #we start at 0 likes when we create a movie
    dislikes = db.Column(db.Integer) #we start at 0  dislikes when we create a movie

    def __init__(self, movie_title, description, release_year, duration, rating, likes, dislikes):

        self.movie_title = movie_title
        self.description = description
        self.release_year = release_year
        self.duration = duration
        self.rating = rating
        self.likes = likes
        self.dislikes = dislikes

# Movie Schema

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'movie_title', 'description', 'release_year', 'duration', 'rating', 'likes', 'dislikes')

#Initialize Schema
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True) #if we are dealing with many movies(list)

#App routes

#Add or create a movie 
@backend_app.route('/movie', methods=['POST'])
def add_movie():
    movie_title = request.json['movie_title']
    description = request.json['description']
    release_year = request.json['release_year']
    duration = request.json['duration']
    rating = request.json['rating']
    likes = request.json['likes']
    dislikes = request.json['dislikes']

    new_movie = Movie(movie_title, description, release_year, duration, rating, likes, dislikes)
    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie)

#Get all movies
@backend_app.route('/movie', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    return_result = movies_schema.dump(all_movies)
    return jsonify(return_result)

#Get single movie by using ID
@backend_app.route('/movie/<id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    return movie_schema.jsonify(movie)

#Search Movie by using Movie Title (query)
@backend_app.route('/movie/<movie_title>')
def show_movie_by_title(movie_title):
    movie = Movie.query.filter_by(movie_title=movie_title).first_or_404()
    return render_template('show_movie_by_title', movie=movie)

#update a movie info
@backend_app.route('/movie/<id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)

    movie_title = request.json['movie_title']
    description = request.json['description']
    release_year = request.json['release_year']
    duration = request.json['duration']
    rating = request.json['rating']
    likes = request.json['likes']
    dislikes = request.json['dislikes']

    movie.movie_title = movie_title
    movie.description = description
    movie.release_year = release_year
    movie.duration = duration
    movie.rating = rating
    movie.likes = likes
    movie.dislikes = dislikes

    db.session.commit()

    return movie_schema.jsonify(movie)

#update likes
@backend_app.route('/movie/<id>', methods=['PUT'])
def update_likes(id):
    setattr(id, 'likes', id.likes + 1)
    db.session.commit()

#update dislikes
@backend_app.route('/movie/<id>', methods=['PUT'])
def update_dislikes(id):
    setattr(id, 'dislikes', id.dislikes + 1)
    db.session.commit()

#Delete a movie
@backend_app.route('/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonify(movie)


#running server

if __name__ == '__main__':
    backend_app.run(debug=True)