#Entry point, initializes application

import sys
from PyQt5 import QtWidgets
from ui_login_page import LoginPage
from ui_main_window import MainWindow
from ui_watchlist_window import WatchlistWindow
class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize pages
        self.login_page = LoginPage()
        self.main_window = MainWindow()

        #Initialize watchlist page
        self.watchlist_window = WatchlistWindow()
        
        # Add pages to QStackedWidget
        self.stack.addWidget(self.login_page)  # Page 0 → login
        self.stack.addWidget(self.main_window)  # Page 1 → homepage
        self.stack.addWidget(self.watchlist_window) # Page 2 
        
        # Go to home page if login is successful
        self.login_page.switch_window.connect(self.show_main_window)

        # Opening page → login page
        self.stack.setCurrentIndex(0)
        self.menuBar().setVisible(False)
        
        #Adding Menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()
        watchlist_menu = menubar.addMenu("Menu")
        open_watchlist_action = QtWidgets.QAction("Watchlist", self)
        open_watchlist_action.triggered.connect(self.show_watchlist_window)
        watchlist_menu.addAction(open_watchlist_action)
               
    def show_main_window(self):
        """ Ana sayfaya geçiş yap """
        self.menuBar().setVisible(True)
        self.stack.setCurrentIndex(1)
        
    def show_watchlist_window(self):
        """Watchlist"""
        self.menuBar().setVisible(True)
        self.stack.setCurrentIndex(2)
        self.watchlist_window.load_watchlist()  #refresh

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

