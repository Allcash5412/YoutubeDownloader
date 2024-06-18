from fastapi import FastAPI
from src.download.router import download as download_router
from src.auth.router import auth as auth_router
from src.home.router import home_page as home_page_router

app = FastAPI()
app.include_router(home_page_router, tags=['User profile'])
app.include_router(download_router, tags=['Download'])
app.include_router(auth_router, tags=['Auth'])

@app.get('/')
def home_page():
    pass
