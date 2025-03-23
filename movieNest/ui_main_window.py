from PyQt5 import QtWidgets, QtGui, QtCore
import random
import movie_database 
USER_ID = 3
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie App")
        self.setGeometry(100, 100, 1200, 800)
        self.setFixedSize(1200, 800)  # Fixed window size
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
        self.genre_comedy = QtWidgets.QCheckBox("Comedy")
        self.genre_drama = QtWidgets.QCheckBox("Drama")
        self.genre_scifi = QtWidgets.QCheckBox("Sci-Fi")
        self.genre_horror = QtWidgets.QCheckBox("Horror")
        self.genre_thriller = QtWidgets.QCheckBox("Thriller")
        
        genre_layout.addWidget(self.genre_action)
        genre_layout.addWidget(self.genre_comedy)
        genre_layout.addWidget(self.genre_drama)
        genre_layout.addWidget(self.genre_scifi)
        genre_layout.addWidget(self.genre_horror)
        genre_layout.addWidget(self.genre_thriller)
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
        self.recommendations_box.setFixedHeight(300)  # Fixed height for recommendations
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
        
        # Create sample movie data (title, rating, genres)
        self.movie_data = []
        genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Thriller"]
        for i in range(1, 101):
            title = f"Movie {i}"
            rating = random.uniform(5.0, 10.0)
            movie_genres = random.sample(genres, random.randint(1, 3))  # Each movie has 1-3 genres
            self.movie_data.append((title, rating, movie_genres))
        
        self.search_button.clicked.connect(self.update_search_results)
        self.load_recommendations()
        self.load_initial_movies()
    
    def update_rating_label(self):
        min_rating = self.rating_slider.value() / 10
        self.rating_label.setText(f"Min Rating: {min_rating:.1f}")
        
    def create_movie_card(self, title, rating, genres, poster_path):
        # Ensure rating is a float
        try:
            rating = float(rating)
        except ValueError:
            rating = 0.0  # Default to 0.0 if conversion fails

        # Create a fixed-size movie card with standardized layout
        movie_widget = QtWidgets.QWidget()
        movie_layout = QtWidgets.QVBoxLayout(movie_widget)
        movie_layout.setContentsMargins(5, 5, 5, 5)
        movie_widget.setFixedSize(160, 280)  # Fixed size for movie cards
        
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
        random_movies = self.db.get_random_movies(limit=50)  # 10 rastgele film al

        if not random_movies:
            print("⚠️ No movies found in the database.")
            return

        # Filmleri ekrana yerleştir
        for i, movie in enumerate(random_movies):
            print(f"Loaded Movie: {movie}")  # Debugging için
            poster_path = "posters/" + movie[3] if movie[3] else "default_poster.jpg"
            movie_card = self.create_movie_card(movie[1], movie[2], movie[4], poster_path)  # Title, Rating, Genres
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
            poster_path = "posters/" + movie[3] if movie[3] else "default_poster.jpg"
            movie_card = self.create_movie_card(movie[1], movie[2], movie[4], "posters" + poster_path)
            self.recommendations_layout.addWidget(movie_card)
        
        # Add stretch to prevent cards from spreading out too much
        self.recommendations_layout.addStretch()
        
    def update_search_results(self):
        query = self.search_bar.text().lower()
        min_rating = self.rating_slider.value() / 10
        
        # Get selected genres
        selected_genres = []
        if self.genre_action.isChecked():
            selected_genres.append("Action")
        if self.genre_comedy.isChecked():
            selected_genres.append("Comedy")
        if self.genre_drama.isChecked():
            selected_genres.append("Drama")
        if self.genre_scifi.isChecked():
            selected_genres.append("Sci-Fi")
        if self.genre_horror.isChecked():
            selected_genres.append("Horror")
        if self.genre_thriller.isChecked():
            selected_genres.append("Thriller")
        
        # Clear previous search results
        for i in reversed(range(self.search_results_layout.count())):
            item = self.search_results_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        # Filter movies based on search, rating, and genres
        filtered_movies = []
        for title, rating, genres in self.movie_data:
            title_match = query == "" or query in title.lower()
            rating_match = rating >= min_rating
            genre_match = not selected_genres or any(g in selected_genres for g in genres)
            
            if title_match and rating_match and genre_match:
                filtered_movies.append((title, rating, genres))
        
        # Display filtered movies
        for i, (title, rating, genres) in enumerate(filtered_movies):
            movie_card = self.create_movie_card(title, rating, genres)
            row = i // 5
            col = i % 5
            self.search_results_layout.addWidget(movie_card, row, col)
        
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