import mysql.connector
import os
import requests

# Veritabanı bağlantısı
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*Tsamil11",
    database="movienest"
)
cursor = conn.cursor()

# Poster URL'lerini çek
cursor.execute("SELECT poster_path FROM Movies")
poster_paths = cursor.fetchall()

# Klasör oluştur (varsa atla)
os.makedirs("posters", exist_ok=True)

# TMDB Base URL
BASE_URL = "https://image.tmdb.org/t/p/w92"

# Posterleri indir
for poster in poster_paths:
    if poster and poster[0]:  # Eğer poster_path boş değilse
        full_url = f"{BASE_URL}{poster[0]}"
        image_name = poster[0].lstrip("/")  # "/" karakterini kaldır
        image_path = os.path.join("posters", image_name)

        # Görseli indir
        response = requests.get(full_url, stream=True)
        if response.status_code == 200:
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"✅ {image_name} indirildi.")
        else:
            print(f"⚠️ {image_name} indirilemedi!")

# Bağlantıyı kapat
cursor.close()
conn.close()
