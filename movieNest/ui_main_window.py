#Home page of the application

from PyQt5 import QtCore, QtGui, QtWidgets
from movie_database import Database 
from PyQt5.QtWidgets import QMessageBox
import traceback

class UiMainWindow(object):
    def __init__(self):
        self.db = Database()  # Make connection at the beginning of the program

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 190, 121, 51))
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 60, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setObjectName("label")

        self.retranslate_ui(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.on_clicked)

    def on_clicked(self):
        """ Butona basınca film bilgisini getir """
        try:
            movie_name = self.db.search_and_filter("four rooms",[],[])
            for l in movie_name:
                print(str(l))
            
        except Exception as err:
            error_message = f"Hata oluştu:\n{str(err)}"
            print(error_message)
            traceback.print_exc()
            QMessageBox.critical(None, "Veritabanı Hatası", error_message)

    def retranslate_ui(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Film Getir"))
        self.label.setText(_translate("Dialog", "Hello World"))
