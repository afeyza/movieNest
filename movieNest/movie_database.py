#Database module for all database queries and actions

import mysql.connector
import traceback
import MySQLdb as mdb

class Database:
    _instance = None 

    def __new__(cls):
        """ Singleton tasarımı: Sadece bir kez bağlantı oluştur. """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        """ MySQL bağlantısını aç ve açık tut """
        try:
            self.db = mdb.connect(
                host="localhost",
                user="root",
                password="*Tsamil11",
                database="movienest"
            )
            self.cursor = self.db.cursor()
            print("✅ Veritabanı bağlantısı başarılı.")
        except mdb.Error as e:
            print(f"⚠️ Veritabanı bağlantı hatası: {e}")
            self.db = None

    def get_movie_title(self, movie_id):
        """ ID'ye göre film başlığını getir """
        try:
            query = "SELECT title FROM Movies WHERE id = %s"
            self.cursor.execute(query, (movie_id,))
            result = self.cursor.fetchone()
            return result[0] if result else "Film bulunamadı."

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Hata oluştu"
        
    def get_movie(self, movie_id):
        """ ID'ye göre filmi getir """
        try:
            query = "SELECT * FROM Movies WHERE id = %s"
            self.cursor.execute(query, (movie_id,))
            result = self.cursor.fetchone()
            return result if result else "Film bulunamadı."

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Hata oluştu"
        
    def get_user(self, user_id):
        """ ID'ye göre user getir """
        try:
            query = "SELECT * FROM Users WHERE id = *"
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result if result else "User bulunamadı."

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Hata oluştu"
        
    def register_user(self, username, password):
        """ Kullanıcıyı veritabanına ekler ve başarılı olup olmadığını kontrol eder """
        try:
            query = "INSERT INTO Users (nickname, password) VALUES (%s, %s);"
            self.cursor.execute(query, (username, password,))
            self.db.commit()

            if self.cursor.rowcount > 0:
                return "✅ Kullanıcı başarıyla kaydedildi."
            else:
                return "❌ Kullanıcı kaydedilemedi."

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Hata oluştu"
        
    def authenticate_user(self, username, password):
        """ Kullanıcı adı ve şifreyi kontrol eden fonksiyon """
        try:
            query = "SELECT * FROM Users WHERE nickname = %s AND password = %s;"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()

            return result is not None

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return False

    def close_connection(self):
        """ Uygulama kapanırken bağlantıyı temizle """
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
            print("✅ Veritabanı bağlantısı kapatıldı.")
