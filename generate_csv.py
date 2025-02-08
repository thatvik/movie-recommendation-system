import pandas as pd
from imdb import IMDb

# Create an instance of the IMDb class
ia = IMDb()

# Search for movies (e.g., the top 50 popular movies)
movies = ia.get_top250_movies()[:50]  # Adjust as needed

# Create a dictionary to hold movie data
data = {
    'title': [],
    'year': [],
    'rating': [],
    'genres': [],
    'plot': [],
    'director': [],
    'cast': []
}

# Fetch movie details for each movie
for movie in movies:
    ia.update(movie)  # Fetch additional details
    data['title'].append(movie.get('title'))
    data['year'].append(movie.get('year'))
    data['rating'].append(movie.get('rating'))
    data['genres'].append(movie.get('genres'))
    data['plot'].append(movie.get('plot'))
    data['director'].append([person['name'] for person in movie.get('directors')])
    data['cast'].append([person['name'] for person in movie.get('cast')[:5]])  # Get top 5 cast members

# Create a DataFrame
movie_df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
movie_df.to_csv('movies_dataset.csv', index=False)

print("CSV file generated successfully.")
