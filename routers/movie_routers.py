from fastapi import APIRouter, HTTPException
from db.models.movie_model import Movie
from db.schemas.movie_schema import movie_schema, movies_schema
from db.db_connection import db_connection
from bson import ObjectId

router = APIRouter(prefix="/api",
                   tags=["Movies"],
                   responses={404: {"message": "Movie not found"}})

def find_movie(field: str, key):
    try:
        movie = db_connection.movies.find_one({field: key})
        return Movie(**movie_schema(movie))
    except:
        return {"Error": "movie not found"}
    
@router.get("/movies", status_code=200)
async def get_all_movies():
    return movies_schema(db_connection.movies.find())

@router.get("/movie/{id}", status_code=200)
async def find_one_movie(id: str):
    try:
        return find_movie("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=404)
    
@router.post("/movie", response_model=Movie, status_code=201)
async def create_movie(movie: Movie) -> Movie:

    movie_dict = dict(movie)
    del movie_dict["id"]

    id = db_connection.movies.insert_one(movie_dict).inserted_id
    new_movie = movie_schema(db_connection.movies.find_one({"_id": id}))
    return Movie(**new_movie)

@router.put("/movie", response_model=Movie, status_code=201)
async def put_movie(movie: Movie):
    
    movie_dict = dict(movie)
    del movie_dict["id"]

    try:
        db_connection.movies.find_one_and_replace({"_id": ObjectId(movie.id)}, movie_dict)
    except:
        raise HTTPException(status_code=400, detail={"Error": "Movie not found"})
    else:
        return find_movie("_id", ObjectId(movie.id))
    
@router.delete("/movie/{id}", status_code=200)
async def delete_movie(id: str):
    try:
        movie_name = find_movie("_id", ObjectId(id)).name
        db_connection.movies.find_one_and_delete({"_id": ObjectId(id)})
        return {"Ok": f"Movie deleted: {movie_name}"}
    except:
        raise HTTPException(status_code=400, detail={"Error": "Movie not found"})