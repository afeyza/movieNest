import requests
import json

# TMDb API Anahtarı
API_KEY = "629994c79321cce87cc370d483a6589e"

# Filmleri çekmek için başlangıç URL'si (ilk sayfa)
url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=tr-TR&page=1"

# Tüm filmleri tutacak liste
all_movies = []

# Sayfa numarası
page_number = 1

# Sayfalama işlemi 
while True:
    # API isteği gönder
    response = requests.get(url)
    
    # API yanıtı başarıyla alındıysa
    if response.status_code == 200:
        data = response.json()
        
        # Film verilerini listeye ekle
        all_movies.extend(data['results'])
        
        # Eğer daha fazla sayfa varsa, sayfa numarasını artır
        if data['page'] < data['total_pages']:
            page_number += 1
            url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=tr-TR&page={page_number}"
        else:
            break  # Tüm sayfalar çekildi, döngüyü bitir
    
    else:
        print(f"❌ API isteği başarısız! Durum Kodu: {response.status_code}")
        break

# Tüm filmleri JSON dosyasına kaydet
with open('all_movies.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_movies, json_file, indent=4, ensure_ascii=False)

print("🎉 Tüm filmler JSON dosyasına kaydedildi!")
