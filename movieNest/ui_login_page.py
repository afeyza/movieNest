#Login page for the user
import ui_watchlist_window
import ui_main_window
from PyQt5 import QtWidgets, QtCore
from movie_database import Database
class LoginPage(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()  # Homepage signal

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.db=Database()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.resize(400, 300)
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("User Name")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        
        self.register_button = QtWidgets.QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db.login_user(username, password):
            id=self.db.get_user_id(username,password)
            ui_main_window.USER_ID=id
            ui_watchlist_window.USER_ID=id
            print("Login successful...")
            self.switch_window.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid username or password!")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter your username and password to register.")
            return

        result = self.db.register_user(username, password)
        QtWidgets.QMessageBox.information(self, "Register", result)