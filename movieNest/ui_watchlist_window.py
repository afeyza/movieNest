from PyQt5 import QtWidgets, QtGui, QtCore
import movie_database 

USER_ID = 3  # Gonna change?

class WatchlistWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = movie_database.Database()
        self.setWindowTitle("Watchlist")
        self.setGeometry(100, 100, 1200, 800)
        self.setFixedSize(1200, 800)  #Fixed size
        self.setStyleSheet("background-color: rgb(255, 122, 105);")
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        
        # Left: Image
        self.image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("watchlistside.png")
        pixmap = pixmap.scaled(300, 800, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(300, 800)
        main_layout.addWidget(self.image_label)
        # Right: Content
        right_layout = QtWidgets.QVBoxLayout()
        


        # Scroll area for movie cards
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        right_layout.addWidget(self.scroll_area)

        main_layout.addLayout(right_layout)
        self.load_watchlist()

    def load_watchlist(self):
        self.watchlist = self.db.get_watchlist(USER_ID)
        if self.watchlist == "Empty Watchlist":
            self.display_empty_message()
            return

        self.display_movies(self.watchlist)

    def display_empty_message(self):
        label = QtWidgets.QLabel("Your watchlist is empty.")
        label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        label.setFont(font)

        # Temizle ve göster
        self.clear_layout(self.scroll_layout)
        self.scroll_layout.addWidget(label, 0, 0)

    def display_movies(self, movie_list):
        self.clear_layout(self.scroll_layout)

        for i, movie in enumerate(movie_list):
            movie_widget = self.create_movie_card(movie)
            row = i // 4
            col = i % 4
            self.scroll_layout.addWidget(movie_widget, row, col)

    def create_movie_card(self, movie):
        movie_id, title, rating, poster_path, genre_ids = movie
         # Ensure rating is a float
        try:
            rating = float(rating)
        except ValueError:
            rating = 0.0  # Default to 0.0 if conversion fails
    
        genres = [self.db.genre_dict[int(g)] for g in genre_ids.split(",") if g.isdigit()]
        genre_text = " | ".join(genres)
        poster_path = "posters/" + poster_path if poster_path else "default_poster.jpg"

        # Main widget
        card = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(5, 5, 5, 5)
        card.setFixedSize(160, 330) #310?

        # Poster
        poster = QtWidgets.QLabel()
        poster.setFixedSize(150, 180)
        
        #Try loading the poster from the given path
        pixmap = QtGui.QPixmap(poster_path)
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(150, 180)
            pixmap.fill(QtGui.QColor("gray"))
        
        poster.setPixmap(pixmap.scaled(150, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        poster.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(poster)

        # Title with fixed height and ellipsis for long titles
        title_label = QtWidgets.QLabel(title)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFixedHeight(20)
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)
        title_label.setWordWrap(False)
        title_label.setTextFormat(QtCore.Qt.PlainText)
        
        # Use elide to handle long text
        metrics = QtGui.QFontMetrics(title_label.font())
        elided_text = metrics.elidedText(title, QtCore.Qt.ElideRight, 140)
        title_label.setText(elided_text)
        layout.addWidget(title_label)
        
        # Genres
        genre_text = " | ".join(genres)
        genre_label = QtWidgets.QLabel()
        genre_label.setFixedHeight(20)
        genre_label.setAlignment(QtCore.Qt.AlignCenter)
       # genre_label.setStyleSheet("font-size: 10px;")
        
        # Use elide to handle long text
        metrics = QtGui.QFontMetrics(genre_label.font())
        elided_genre = metrics.elidedText(genre_text, QtCore.Qt.ElideRight, 140)
        genre_label.setText(elided_genre)
        layout.addWidget(genre_label)

        # Rating
        rating_label = QtWidgets.QLabel(f"IMDb: {rating:.1f}")
        rating_label.setFixedHeight(20)
        rating_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(rating_label)

        # Remove checkbox
        #checkbox = QtWidgets.QCheckBox("Remove")
        #checkbox.stateChanged.connect(lambda state: self.handle_removal(state, movie_id, card)) #dinemic
        #layout.addWidget(checkbox)

        # Remove from watchlist button
        remove_button = QtWidgets.QPushButton("Remove from Watchlist")
        remove_button.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        remove_button.clicked.connect(lambda: self.handle_removal(movie_id, card))
        layout.addWidget(remove_button)
        
        card.setStyleSheet("border: 1px solid gray; background-color: white; border-radius: 5px;")
        return card

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def remove_from_watchlist(self, movie_id):
        self.db.remove_movie(USER_ID, movie_id)
        self.load_watchlist()
        
    def handle_removal(self, movie_id, card):
        confirm = QtWidgets.QMessageBox.question(
            self, "Onay", "Bu filmi watchlist'ten silmek istiyor musun?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            self.remove_from_watchlist(movie_id, card)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = WatchlistWindow()
    window.show()
    app.exec_()