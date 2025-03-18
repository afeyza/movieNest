#Database module for all database queries and actions

import mysql.connector
import traceback
import MySQLdb as mdb
from PyQt5.QtWidgets import QMessageBox

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
        
    def get_random_movies(self, limit=100):
        """ Fetch 100 random movies from the database """
        try:
            query = f"SELECT * FROM movies ORDER BY RAND() LIMIT %s"
            self.cursor.execute(query, (limit,))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"⚠️ Database error: {err}")
            traceback.print_exc()
            return None
        
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
        """ Kullanıcıyı veritabanına eklerken, kullanıcı adının önceden alınmış olup olmadığını kontrol eder """
        try:
            # Kullanıcı adı daha önce kullanılmış mı kontrol et
            check_query = "SELECT COUNT(*) FROM Users WHERE nickname = %s"
            self.cursor.execute(check_query, (username,))
            user_exists = self.cursor.fetchone()[0] > 0

            if user_exists:
                return "❌ Bu kullanıcı adı zaten alınmış, lütfen başka bir tane deneyin."

            # Kullanıcı adı kullanılabilir, kaydı yap
            query = "INSERT INTO Users (nickname, password) VALUES (%s, %s);"
            self.cursor.execute(query, (username, password))
            self.db.commit()

            if self.cursor.rowcount > 0:
                return "✅ Kullanıcı başarıyla kaydedildi."
            else:
                return "❌ Kullanıcı kaydedilemedi."

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Hata oluştu"

        
    def login_user(self, username, password):
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


    """ 
    Verilen user_id parametresine göre kullanıcıya ait izleme listesini döner.
    İzleme listesi boşsa "Empty Watchlist" stringi döner.
    """
    def get_watchlist(self, user_id):
        try:
            query = """
            SELECT m.id, m.title, vote_average, poster_path, genre_ids
            FROM user_movie_list l 
            JOIN movies m ON l.movie_id = m.id 
            WHERE l.user_id = %s
            """
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchall() 

            if not result:
                return "Empty Watchlist"
        
            return result
        
        except Exception as e:
            error_message = f"Hata oluştu: {e}"
            QMessageBox.critical(None, "Hata", error_message)
            
        
        
    """
    Verilen user_id için kullanıcının izleme listesine movie_id bilgisine sahip filmi ekler.
    Ekleme işlemi başarılıysa 1 döner.
    Film zaten ekliyse uyarı verir, 0 döner.
    """
    def add_movie(self, user_id, movie_id):
        try:
           watchlist = self.get_watchlist(user_id)
           for movie in watchlist:
               if(movie[0] == movie_id):
                    error_message = "Seçili film zaten listenizde ekli!"
                    QMessageBox.critical(None, "Uyarı", error_message)
                    return 0

           query = """
           INSERT INTO user_movie_list (user_id, movie_id)
           VALUES (%s, %s);
           """
           self.cursor.execute(query, (user_id, movie_id))
           self.db.commit()  
           return 1  
        
        except Exception as e:
            error_message = f"Hata oluştu: {e}"
            QMessageBox.critical(None, "Hata", error_message)
            return 0
        
        
    """
    Verilen user_id bilgisine sahip kullanıcının izleme listesinden movie_id bilgisine sahip filmi siler.
    İşlem başarılı ise 1 döner.
    """
    def remove_movie(self, user_id, movie_id):
        try:
            query = """
            DELETE FROM user_movie_list l
            WHERE l.user_id = %s 
            AND l.movie_id = %s;
            """
            self.cursor.execute(query, (user_id, movie_id))
            self.db.commit() 
            return 1
        
        except Exception as e:
            error_message = f"Hata oluştu: {e}"
            QMessageBox.critical(None, "Hata", error_message)
            return 0
        
 
## search_and_filter(genre[], rating[])  return [][]: Makes a filtering operation on the movie list based on the genre and rating filtering options. Returns the filtered movie list.
	
## search(title) return [][]: Searches the given title in the movie list and returns the results.
    """
    Seçilen türlere ve oylama(puan) aralıklarına göre filtreleme yapar.
    Verilen aralıklardan ve türlerden herhangi birine sahip olan filmler getirilir.
    Filtre uygulanmamış alanlar tüm tür veya aralık değerleri üzerinden incelenir.
    Filtre yapılmadıysa tüm filmleri getirmek için filter([], []) şeklinde kullanılabilir.
    Sonuç liste halinde dönülür.
    """
    def filter(self, genres, vote_ranges):
        try:
            if(genres != [] and vote_ranges != []):
                vote_conditions = " OR ".join(["(vote_average BETWEEN %s AND %s)"] * len(vote_ranges))
                genre_conditions = " OR ".join(["(genre_ids = %s)"] * len(genres))
                query = f"""
                SELECT * 
                FROM movies 
                WHERE ({vote_conditions})
                AND ({genre_conditions})
                """    
                vote_params = [value for r in vote_ranges for value in r] 
                genre_params = [value for value in genres] 
                self.cursor.execute(query, (tuple(vote_params) + tuple(genre_params)))

            elif(genres != []):
                genre_conditions = " OR ".join(["(genre_ids = %s)"] * len(genres))
                query = f"""    
                SELECT * 
                FROM movies 
                WHERE {genre_conditions}
                """
                genre_params = [value for value in genres] 
                self.cursor.execute(query, tuple(genre_params))

            elif(vote_ranges != []):
                vote_conditions = " OR ".join(["(vote_average BETWEEN %s AND %s)"] * len(vote_ranges))
                query = f"""    
                SELECT * 
                FROM movies 
                WHERE {vote_conditions}
                """
                vote_params = [value for r in vote_ranges for value in r] 
                self.cursor.execute(query, tuple(vote_params))

            else:
                query = f"""    
                SELECT * 
                FROM movies 
                """
                self.cursor.execute(query)

            return self.cursor.fetchall()
        
        except Exception as e:
            error_message = f"Hata oluştu: {e}"
            QMessageBox.critical(None, "Hata", error_message)
            return "Hata"








