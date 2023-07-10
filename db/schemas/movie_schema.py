def movie_schema(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "name": movie["name"],
        "genres": movie["genres"],
        "url": movie["url"]
    }

def movies_schema(movies) -> dict:
    return [movie_schema(movie) for movie in movies]