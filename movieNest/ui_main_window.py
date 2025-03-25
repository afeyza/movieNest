from PyQt5 import QtWidgets, QtGui, QtCore
import random
import movie_database 
from PyQt5.QtWidgets import QMessageBox
USER_ID = 1

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie App")
        self.setGeometry(100, 100, 1200, 900)
        self.setFixedSize(1200, 900)  # Fixed window size
        self.db = movie_database.Database()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        
        # Left column: Filters
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Genre filter section
        self.genre_box = QtWidgets.QGroupBox("Genre")
        genre_layout = QtWidgets.QVBoxLayout()
        self.genre_action = QtWidgets.QCheckBox("Action")
        self.genre_adventure = QtWidgets.QCheckBox("Adventure")
        self.genre_animation = QtWidgets.QCheckBox("Animation")
        self.genre_comedy = QtWidgets.QCheckBox("Comedy")
        self.genre_crime = QtWidgets.QCheckBox("Crime")
        self.genre_documentary = QtWidgets.QCheckBox("Documentary")
        self.genre_drama = QtWidgets.QCheckBox("Drama")
        self.genre_family = QtWidgets.QCheckBox("Family")
        self.genre_fantasy = QtWidgets.QCheckBox("Fantasy")
        self.genre_history = QtWidgets.QCheckBox("History")
        self.genre_horror = QtWidgets.QCheckBox("Horror")
        self.genre_music = QtWidgets.QCheckBox("Music")
        self.genre_mystery = QtWidgets.QCheckBox("Mystery")
        self.genre_romance = QtWidgets.QCheckBox("Romance")
        self.genre_scifi = QtWidgets.QCheckBox("Sci-Fi")
        self.genre_thriller = QtWidgets.QCheckBox("Thriller")
        self.genre_tvmovie = QtWidgets.QCheckBox("TV Movie")
        self.genre_war = QtWidgets.QCheckBox("War")
        self.genre_western = QtWidgets.QCheckBox("Western")

        
        genre_layout.addWidget(self.genre_action)
        genre_layout.addWidget(self.genre_adventure)
        genre_layout.addWidget(self.genre_animation)
        genre_layout.addWidget(self.genre_comedy)
        genre_layout.addWidget(self.genre_crime)
        genre_layout.addWidget(self.genre_documentary)
        genre_layout.addWidget(self.genre_drama)
        genre_layout.addWidget(self.genre_family)
        genre_layout.addWidget(self.genre_fantasy)
        genre_layout.addWidget(self.genre_history)
        genre_layout.addWidget(self.genre_horror)
        genre_layout.addWidget(self.genre_music)
        genre_layout.addWidget(self.genre_mystery)
        genre_layout.addWidget(self.genre_romance)
        genre_layout.addWidget(self.genre_scifi)
        genre_layout.addWidget(self.genre_thriller)
        genre_layout.addWidget(self.genre_tvmovie)
        genre_layout.addWidget(self.genre_war)
        genre_layout.addWidget(self.genre_western)


        genre_layout.addStretch()
        self.genre_box.setLayout(genre_layout)
        left_layout.addWidget(self.genre_box)
        
        # IMDb rating filter section
        self.rating_box = QtWidgets.QGroupBox("IMDb Rating")
        rating_layout = QtWidgets.QVBoxLayout()
        
        self.rating_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rating_slider.setMinimum(0)
        self.rating_slider.setMaximum(100)
        self.rating_slider.setValue(50)  # Default to 5.0
        
        self.rating_label = QtWidgets.QLabel("Min Rating: 5.0")
        self.rating_slider.valueChanged.connect(self.update_rating_label)
        
        rating_layout.addWidget(self.rating_label)
        rating_layout.addWidget(self.rating_slider)
        
        self.rating_box.setLayout(rating_layout)
        left_layout.addWidget(self.rating_box)
        
        # Apply filters button
        self.apply_button = QtWidgets.QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self.update_search_results)
        left_layout.addWidget(self.apply_button)
        
        left_layout.addStretch()  # Fill remaining space
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(250)  # Fixed width for filter panel
        main_layout.addWidget(left_widget)
        
        # Right section: Split into two parts (upper and lower)
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # Search bar at the top of right section
        search_layout = QtWidgets.QHBoxLayout()
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search for movies...")
        search_layout.addWidget(self.search_bar)
        self.search_button = QtWidgets.QPushButton("Search")
        search_layout.addWidget(self.search_button)
        right_layout.addLayout(search_layout)
        
        # Upper part: Recommendations
        self.recommendations_box = QtWidgets.QGroupBox("Recommendations")
        recommendations_container = QtWidgets.QVBoxLayout()
        self.recommendations_content = QtWidgets.QWidget()
        self.recommendations_layout = QtWidgets.QHBoxLayout(self.recommendations_content)
        self.recommendations_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.recommendations_layout.setSpacing(20)  # Space between movie cards
        recommendations_container.addWidget(self.recommendations_content)
        self.recommendations_box.setLayout(recommendations_container)
        self.recommendations_box.setFixedHeight(350)  # Fixed height for recommendations
        right_layout.addWidget(self.recommendations_box)
        
        # Lower part: Search results (scrollable)
        self.search_results_box = QtWidgets.QGroupBox("Search Results")
        search_results_container = QtWidgets.QVBoxLayout()
        self.search_results_scroll = QtWidgets.QScrollArea()
        self.search_results_scroll.setWidgetResizable(True)
        self.search_results_content = QtWidgets.QWidget()
        self.search_results_layout = QtWidgets.QGridLayout(self.search_results_content)
        self.search_results_layout.setHorizontalSpacing(20)  # Space between columns
        self.search_results_layout.setVerticalSpacing(20)    # Space between rows
        self.search_results_scroll.setWidget(self.search_results_content)
        search_results_container.addWidget(self.search_results_scroll)
        self.search_results_box.setLayout(search_results_container)
        right_layout.addWidget(self.search_results_box)
        
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget)
        
        self.search_button.clicked.connect(self.apply_title_search)
        self.load_recommendations()
        self.load_initial_movies()
    
    def update_rating_label(self):
        min_rating = self.rating_slider.value() / 10
        self.rating_label.setText(f"Min Rating: {min_rating:.1f}")
    
    def add_to_watchlist(self, movie_id):
        # This function would add the movie to the user's watchlist in the database
        # For now, just show a message indicating success
        
        result = self.db.add_movie(USER_ID, movie_id)
        if result == 1:
            QMessageBox.information(self, "Success", f"Movie added to your watchlist!")
            
        
    def create_movie_card(self, title, rating, genres_string, poster_path, movie_id=None):
        # Ensure rating is a float
        try:
            rating = float(rating)
        except ValueError:
            rating = 0.0  # Default to 0.0 if conversion fails

        if genres_string:
            genre_ids = [int(num.strip()) for num in genres_string.split(",") if num.strip().isdigit()]#in case of genres_string being empty or None
        else:
            genre_ids = []
        genres = []
        for genre_id in genre_ids:
            genres.append(self.db.genre_dict[genre_id])
        # Create a fixed-size movie card with standardized layout
        movie_widget = QtWidgets.QWidget()
        movie_layout = QtWidgets.QVBoxLayout(movie_widget)
        movie_layout.setContentsMargins(5, 5, 5, 5)
        movie_widget.setFixedSize(160, 310)  # Increase height for Add button
        
        # Poster with fixed size
        poster = QtWidgets.QLabel()
        poster.setFixedSize(150, 180)

        # Try loading the poster from the given path
        pixmap = QtGui.QPixmap(poster_path)
        if pixmap.isNull():  # If loading fails, use a placeholder
            pixmap = QtGui.QPixmap(150, 180)
            pixmap.fill(QtGui.QColor("gray"))

        poster.setPixmap(pixmap.scaled(150, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        poster.setAlignment(QtCore.Qt.AlignCenter)
        movie_layout.addWidget(poster)
        
        # Title with fixed height and ellipsis for long titles
        title_label = QtWidgets.QLabel(title)
        title_label.setFixedHeight(20)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)
        title_label.setWordWrap(False)
        title_label.setTextFormat(QtCore.Qt.PlainText)
        
        # Use elide to handle long text
        metrics = QtGui.QFontMetrics(title_label.font())
        elided_text = metrics.elidedText(title, QtCore.Qt.ElideRight, 140)
        title_label.setText(elided_text)
        movie_layout.addWidget(title_label)
        
        # Genre with fixed height and ellipsis
        genre_text = " | ".join(genres)
        genre_label = QtWidgets.QLabel()
        genre_label.setFixedHeight(20)
        genre_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Use elide to handle long text
        metrics = QtGui.QFontMetrics(genre_label.font())
        elided_genre = metrics.elidedText(genre_text, QtCore.Qt.ElideRight, 140)
        genre_label.setText(elided_genre)
        movie_layout.addWidget(genre_label)
        
        # Rating with fixed height
        imdb_label = QtWidgets.QLabel(f"IMDb: {rating:.1f}")
        imdb_label.setFixedHeight(20)
        imdb_label.setAlignment(QtCore.Qt.AlignCenter)
        movie_layout.addWidget(imdb_label)
        
        # Add the "Add to Watchlist" button
        if movie_id is not None:
            add_button = QtWidgets.QPushButton("+ Add to Watchlist")
            add_button.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
            add_button.clicked.connect(lambda: self.add_to_watchlist(movie_id))
            movie_layout.addWidget(add_button)
        
        # Set a frame around the movie card
        movie_widget.setStyleSheet("border: 1px solid #cccccc; border-radius: 5px; background-color: #f9f9f9;")
        
        return movie_widget

    def load_initial_movies(self):
        """Load initial random movies into the search results layout when the app starts"""
        # Önceki içeriği temizle
        for i in reversed(range(self.search_results_layout.count())):
            item = self.search_results_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Rastgele filmleri veritabanından çek
        random_movies = self.db.get_random_movies(limit=50) 

        if not random_movies:
            print("⚠ No movies found in the database.")
            return

        # Filmleri ekrana yerleştir
        for i, movie in enumerate(random_movies):
            print(f"Loaded Movie: {movie}")  # Debugging için
            movie_id = movie[0]  # Assuming the first element is the movie ID
            poster_path = "posters/" + movie[3] if movie[3] else "default_poster.jpg"
            movie_card = self.create_movie_card(movie[1], movie[2], movie[4], poster_path, movie_id)
            row = i // 5  # 5'li kolon düzeni
            col = i % 5
            self.search_results_layout.addWidget(movie_card, row, col)

        # Boş alanı dolduracak bir spacer ekle
        if random_movies:
            self.search_results_layout.addItem(
                QtWidgets.QSpacerItem(20, 20, 
                                    QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding),
                (len(random_movies) // 5) + 1, 0
            )
            
    def load_recommendations(self):
        # Clear previous recommendations
        for i in reversed(range(self.recommendations_layout.count())):
            self.recommendations_layout.itemAt(i).widget().setParent(None)
        
        # Show 5 random movies
        selected_movies = self.db.recommend_movie(USER_ID)
        for movie in selected_movies[1]:
            movie_id = movie[0]  # Assuming the first element is the movie ID
            poster_path = "posters/" + movie[3] if movie[3] else "default_poster.jpg"
            movie_card = self.create_movie_card(movie[1], movie[2], movie[4], poster_path, movie_id)
            self.recommendations_layout.addWidget(movie_card)
        
        # Add stretch to prevent cards from spreading out too much
        self.recommendations_layout.addStretch()
        
    def update_search_results(self):
        query = self.search_bar.text().lower().strip()
        min_rating = self.rating_slider.value() / 10
        
        # Get selected genres
        selected_genres = []
        if self.genre_action.isChecked():
            selected_genres.append(28)
        if self.genre_adventure.isChecked():
            selected_genres.append(12)
        if self.genre_animation.isChecked():
            selected_genres.append(16)
        if self.genre_comedy.isChecked():
            selected_genres.append(35)
        if self.genre_crime.isChecked():
            selected_genres.append(80)
        if self.genre_documentary.isChecked():
            selected_genres.append(99)
        if self.genre_drama.isChecked():
            selected_genres.append(18)
        if self.genre_family.isChecked():
            selected_genres.append(10751)
        if self.genre_fantasy.isChecked():
            selected_genres.append(14)
        if self.genre_history.isChecked():
            selected_genres.append(36)
        if self.genre_horror.isChecked():
            selected_genres.append(27)
        if self.genre_music.isChecked():
            selected_genres.append(10402)
        if self.genre_mystery.isChecked():
            selected_genres.append(9648)
        if self.genre_romance.isChecked():
            selected_genres.append(10749)
        if self.genre_scifi.isChecked():
            selected_genres.append(878)
        if self.genre_thriller.isChecked():
            selected_genres.append(53)
        if self.genre_tvmovie.isChecked():
            selected_genres.append(10770)
        if self.genre_war.isChecked():
            selected_genres.append(10752)
        if self.genre_western.isChecked():
            selected_genres.append(37)

        
        # Clear previous search results
        for i in reversed(range(self.search_results_layout.count())):
            item = self.search_results_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        # Filter movies based on search, rating, and genres
        filtered_movies = self.db.search_and_filter(query, selected_genres, [(min_rating, 10)])

        if(filtered_movies == "Something went wrong"):
            QMessageBox.critical(None, "Error", "Something went wrong")
            return "Error"
        
        # Display filtered movies
        i = 0
        for movie in filtered_movies:
            movie_id = movie[0]  # Assuming the first element is the movie ID
            poster_path = "posters/" + movie[3] if movie[3] else "default_poster.jpg"
            movie_card = self.create_movie_card(movie[1], movie[2], movie[4], poster_path, movie_id)
            row = i // 5
            col = i % 5
            self.search_results_layout.addWidget(movie_card, row, col)
            i = i+1
        
        # Add an empty widget to fill remaining space
        if filtered_movies:
            self.search_results_layout.addItem(
                QtWidgets.QSpacerItem(20, 20, 
                                      QtWidgets.QSizePolicy.Expanding,
                                      QtWidgets.QSizePolicy.Expanding),
                (len(filtered_movies) // 5) + 1, 0)
            
    def apply_title_search(self):
        query = self.search_bar.text().lower().strip()
        
        # Clear previous search results
        for i in reversed(range(self.search_results_layout.count())):
            item = self.search_results_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        filtered_movies = self.db.search(query)

        if(filtered_movies == "Error"):
            QMessageBox.critical(None, "Error", "Something went wrong")
            return "Error"
        
        # Display filtered movies
        i = 0
        for movie in filtered_movies:
            movie_id = movie[0]  # Assuming the first element is the movie ID
            poster_path = "posters/" + movie[3] if movie[3] else "default_poster.jpg"
            movie_card = self.create_movie_card(movie[1], movie[2], movie[4], poster_path, movie_id)
            row = i // 5
            col = i % 5
            self.search_results_layout.addWidget(movie_card, row, col)
            i = i+1
        
        # Add an empty widget to fill remaining space
        if filtered_movies:
            self.search_results_layout.addItem(
                QtWidgets.QSpacerItem(20, 20, 
                                      QtWidgets.QSizePolicy.Expanding,
                                      QtWidgets.QSizePolicy.Expanding),
                (len(filtered_movies) // 5) + 1, 0)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()