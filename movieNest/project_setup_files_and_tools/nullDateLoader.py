import mysql.connector
import json

# MySQL bağlantısı
conn = mysql.connector.connect(
    host="localhost",  # Host adı (genelde localhost)
    user="root",       # Kullanıcı adı (örneğin: root)
    password="*Tsamil11",  # Parola
    database="movienest"   # Veritabanı adı
)

cursor = conn.cursor()

# JSON dosyasını oku
try:
    with open('all_movies.json', 'r', encoding='utf-8') as file:
        json_data = file.read()  # Dosya içeriğini oku

    # JSON verisini parse et
    data = json.loads(json_data)

    # Verileri veritabanına yükle
    for movie in data:
        # Eğer release_date 'NULL' ise, veriyi ekleyelim
        if movie['release_date'] == 'NULL':
            try:
                # Veritabanına eklemek için SQL sorgusu
                sql = """INSERT INTO Movies (
                            id, title, original_title, overview, release_date, vote_average, 
                            vote_count, poster_path, backdrop_path, popularity,
                            original_language, video, adult, genre_ids
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                # Genre ids array'i string olarak saklanabilir
                genre_ids = ', '.join(map(str, movie['genre_ids']))

                # release_date'i NULL olarak göndereceğiz
                release_date = None  # NULL olarak kabul edilecek
                
                # Verileri tuple şeklinde hazırlama
                values = (
                    movie['id'],
                    movie['title'],
                    movie['original_title'],
                    movie['overview'],
                    release_date,  # NULL değeri burada
                    movie['vote_average'],
                    movie['vote_count'],
                    movie['poster_path'],
                    movie['backdrop_path'],
                    movie['popularity'],
                    movie['original_language'],
                    movie['video'],
                    movie['adult'],
                    genre_ids  # Genre IDs burada string olarak saklanıyor
                )

                # Veriyi tabloya ekle
                cursor.execute(sql, values)

            except mysql.connector.Error as err:
                print(f"Veri eklenirken bir hata oluştu: {err}")

    # Değişiklikleri kaydet
    conn.commit()
    print("NULL olan release_date'li veriler başarıyla eklendi.")

except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
except FileNotFoundError:
    print("JSON dosyası bulunamadı.")
except Exception as e:
    print(f"Bir hata oluştu: {e}")
finally:
    # Bağlantıyı kapat
    cursor.close()
    conn.close()
