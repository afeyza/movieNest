#A test module for testing the backend functions without any UI
from movie_database import Database

db = Database()
movie = db.register_user("ahmet","7575")
print(movie)