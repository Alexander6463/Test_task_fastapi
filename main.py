import os

from fastapi import FastAPI
from src.users import router
import uvicorn

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    # uvicorn.run("main:app", host=os.environ.get("HOST"), port=os.environ.get("PORT"))
