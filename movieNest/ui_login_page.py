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
        self.username_input.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QtWidgets.QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db.login_user(username, password):
            id=self.db.get_user_id(username,password)
            ui_main_window.USER_ID=id
            ui_watchlist_window.USER_ID=id
            print("✅ Giriş başarılı! Ana sayfaya geçiliyor...")
            self.switch_window.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")
