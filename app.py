from flask import Flask, request, render_template
from imdb import IMDb
from celery import Celery
import pandas as pd
import os

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

ia = IMDb()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_movie():
    user_input = request.form['movie_title']
    movies = ia.search_movie(user_input)
    
    if not movies:
        return "Movie not found!"
    
    movie = movies[0]
    ia.update(movie)
    
    movie_details = {
        'title': movie['title'],
        'year': movie.get('year'),
        'genres': movie.get('genres'),
        'rating': movie.get('rating'),
        'plot': movie.get('plot')[0] if movie.get('plot') else "No plot available"
    }
    
    return render_template('result.html', movie_details=movie_details)

@celery.task
def update_movie_dataset():
    # Implement the logic to fetch and update movie data
    movies = ia.search_movie('')  # Search for all movies or use a specific query
    data = {
        'title': [],
        'year': [],
        'rating': [],
        'genres': [],
        'plot': [],
        'director': [],
        'cast': []
    }
    
    for movie in movies:
        ia.update(movie)
        data['title'].append(movie.get('title'))
        data['year'].append(movie.get('year'))
        data['rating'].append(movie.get('rating'))
        data['genres'].append(movie.get('genres'))
        data['plot'].append(movie.get('plot'))
        data['director'].append([person['name'] for person in movie.get('directors')])
        data['cast'].append([person['name'] for person in movie.get('cast')[:5]])
    
      


if __name__ == '__main__':
    app.run(debug=True)

    from apscheduler.schedulers.blocking import BlockingScheduler

def update_data():
    # Your scraping or API-fetching code here
    pass

scheduler = BlockingScheduler()
scheduler.add_job(update_data, 'interval', hours=24)  # Update every 24 hours
scheduler.start()



