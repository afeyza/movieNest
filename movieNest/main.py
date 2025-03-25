#Entry point, initializes application

import sys
from PyQt5 import QtWidgets
from ui_login_page import LoginPage
from ui_main_window import MainWindow

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize pages
        self.login_page = LoginPage()
        self.main_window = MainWindow()


        # Add pages to QStackedWidget
        self.stack.addWidget(self.login_page)  # Page 0 → login
        self.stack.addWidget(self.main_window)  # Page 1 → homepage

        # Go to home page if login is successful
        self.login_page.switch_window.connect(self.show_main_window)

        # Opening page → login page
        self.stack.setCurrentIndex(0)

    def show_main_window(self):
        """ Ana sayfaya geçiş yap """
        self.stack.setCurrentIndex(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
