#Login page for the user

from PyQt5 import QtWidgets, QtCore

class LoginPage(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()  # Homepage signal

    def __init__(self):
        super().__init__()
        self.setup_ui()

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

        if username == "admin" and password == "1234":  # Check the username and password
            print("✅ Giriş başarılı! Ana sayfaya geçiliyor...")
            self.switch_window.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")
