from fastapi import APIRouter
from starlette.responses import HTMLResponse

download = APIRouter(prefix='/download')


@download.get('/video', response_class=HTMLResponse)
async def root():
    return {"message": "Hello World"}


@download.get('/playlist', response_class=HTMLResponse)
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
