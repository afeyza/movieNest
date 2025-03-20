#A test module for testing the backend functions without any UI
from movie_database import Database

db = Database()
movies = db.get_random_movies(3)
print(movies)
print("---------")
print(db.sort("alphabetic", "dsc", movies))