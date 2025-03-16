#May not be used in the future

genre_dict = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

# Genre ID'leri anlamlandırmak için
def get_genres(genre_ids):
    return [genre_dict.get(genre_id, "Unknown") for genre_id in genre_ids]

# Örnek kullanım
movie_genres = get_genres([28, 12, 35])  # Action, Adventure, Comedy
print(movie_genres)