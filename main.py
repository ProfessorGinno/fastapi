from fastapi import FastAPI
from routers import movie_routers


app = FastAPI()

app.include_router(movie_routers.router)