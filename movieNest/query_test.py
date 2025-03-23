#A test module for testing the backend functions without any UI
from movie_database import Database

db = Database()
db.add_movie(3, 5)
db.remove_movie(3, 28)
movies = db.recommend_movie(3)
print(movies)
