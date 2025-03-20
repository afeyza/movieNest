#Database module for all database queries and actions

import mysql.connector
import traceback
import MySQLdb as mdb
from PyQt5.QtWidgets import QMessageBox
import re

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
                password="Mysql_sifrem1",
                database="movieNest_481"
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
            error_message = f"Error occured: {e}"
            QMessageBox.critical(None, "Error", error_message)
            
        
        
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
                    error_message = "This movie has already been added to your watchlist!"
                    QMessageBox.critical(None, "Warning", error_message)
                    return 0

           query = """
           INSERT INTO user_movie_list (user_id, movie_id)
           VALUES (%s, %s);
           """
           self.cursor.execute(query, (user_id, movie_id,))
           self.db.commit()  
           return 1  
        
        except Exception as e:
            error_message = f"Error occured: {e}"
            QMessageBox.critical(None, "Error", error_message)
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
            self.cursor.execute(query, (user_id, movie_id,))
            self.db.commit() 
            return 1
        
        except Exception as e:
            error_message = f"Error occured: {e}"
            QMessageBox.critical(None, "Error", error_message)
            return 0
        
	
    """
    genres: seçilen tür filtreleri
    vote_ranges: seçilen oy aralıkları
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
                query = """    
                SELECT * 
                FROM movies 
                """
                self.cursor.execute(query)

            return self.cursor.fetchall()
        
        except Exception as e:
            error_message = f"Error occured: {e}"
            QMessageBox.critical(None, "Error", error_message)
            return "Error"

    """
    title: aranan kelime/kelimeler
    "İçereni bul" şeklinde çalışır.
    Kelimeyi başlığında içeren tüm filmleri saklar.
    Kelimenin başka bir kelimeye dahil olmadığı başlıkları filtrelemek için ilgili fonksiyonu çağırır.
    """
    def search(self, title):    
        try:
             # Kelimenin başlık içinde geçtiği tüm filmleri al
            query = """
            SELECT * 
            FROM movies
            WHERE LOWER(title) LIKE LOWER(%s)
            """
            self.cursor.execute(query, (f"%{title}%",))
            movies = self.cursor.fetchall()
            
            filtered_movies = self.control_for_special_chars(title.lower(), movies)
            
            return filtered_movies
                   
        except Exception as e:
            error_message = f"Error occured: {e}"
            QMessageBox.critical(None, "Error", error_message)
            return "Error"
    """
    searching_title: aranan kelime/kelimeler
    movies: kelimenin geçtiği film listesi
    "İçereni bul" aramasına göre tutulan film başlıklarını inceler.
    Başlıktaki özel karakterleri boşluğa çevirir.
    Aranan kelime başka bir kelimenin içinde geçiyorsa o filmi saklamaz.
    Tek başına kelimeyi bulunduran filmler tutulur.
    Elde edilen film listesi dönülür. 
    """
    def control_for_special_chars(self, searching_title, movies):
        # Kelimenin tam olarak geçmesi durumunda eklendiği liste ("Eve gitti." cümlesi üzerinde "Ev" ile arama yapılırsa film eklenmez.)
        movie_list = []
 
        for movie in movies:
            title = self.replace_special_characters(movie[1].lower())
            
            if(title.startswith(searching_title+" ")):
                movie_list.append(movie)
            elif(title.endswith(" "+searching_title)):
                movie_list.append(movie)
            elif(title.find(" "+searching_title+" ") != -1):
                movie_list.append(movie)
            elif(title == searching_title):
                movie_list.append(movie)

        return movie_list
    """
    input_string: özel karakterleri boşluğa çevrilecek string
    Tüm özel karakterler boşluk karakteri ile değiştirilir.
    """
    def replace_special_characters(self, input_string):
        # Tüm özel karakterleri boşluk (' ') ile değiştiriyoruz
        return re.sub(r'\W', ' ', input_string)
    
    """
    title: seçili kelime filtresi
    genres: seçili tür filtreleri
    vote_ranges: seçili oy aralıkları
    Verilen filtrelere uygun film listesini döner.
    """
    def search_and_filter(self, title, genres, vote_ranges):
        # Tür ve oya göre filtrelenmiş liste
        movies = self.filter(genres, vote_ranges)
        if(movies == "Error"):
            return "Something went wrong"

        filtered_movies = self.control_for_special_chars(title, movies)
        return filtered_movies
    def sort(self, sort_type, order, movies):
        """ Filmleri belirtilen türde ve sırada sıralar """
        reverse = order == "dsc"  # For descending order reverse=True
        if sort_type == "rating":
            sorted_movies = sorted(movies, key=lambda x: x[2], reverse=reverse)  # Rating order
        elif sort_type == "alphabetic":
            sorted_movies = sorted(movies, key=lambda x: x[1].lower(), reverse=reverse)  # Alphabetical order
        else:
            return "❌ Geçersiz sıralama türü!"

        return sorted_movies
    
    def get_poster(self, movie_id):
        """ ID'ye göre film posterini getir """
        try:
            query = "SELECT poster_path FROM Movies WHERE id = %s"
            self.cursor.execute(query, (movie_id,))
            result = self.cursor.fetchone()
            return result[0] if result else "Poster bulunamadı."

        except mysql.connector.Error as err:
            print(f"⚠️ Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Hata oluştu"

