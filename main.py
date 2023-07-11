from fastapi import FastAPI
from routers import movie_routers, user_routers


app = FastAPI()

app.include_router(movie_routers.router)
app.include_router(user_routers.router)