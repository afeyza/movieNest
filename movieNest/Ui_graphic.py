#An example page thats' only purpose is showing a movie poster

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
from movie_database import Database


class ImageViewer(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        # QLabel oluştur ve resmi yükle
        label = QLabel(self)
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print("⚠️ Resim yüklenemedi! Dosya yolunu kontrol edin.")
            return
        
        label.setPixmap(pixmap)
        self.setCentralWidget(label)

        # Pencere boyutunu ayarla
        self.resize(pixmap.width(), pixmap.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database()
    image_path = "posters" + db.get_poster(98)
    viewer = ImageViewer(image_path)
    viewer.show()

    sys.exit(app.exec_())