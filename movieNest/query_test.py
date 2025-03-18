#A test module for testing the backend functions without any UI
from movie_database import Database

db = Database()
movies = db.register_user("ayşe","7")
print(movies)