from fastapi import FastAPI
from cocktail_api import routes

app = FastAPI()

app.include_router(routes.router)