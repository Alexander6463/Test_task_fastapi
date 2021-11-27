import os

from fastapi import FastAPI
from src.users import router
from src.log import configure_logging
import uvicorn

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    logger = configure_logging("log_file.log")
    uvicorn.run(
        "main:app",
        host=os.environ.get("HOST"),
        port=os.environ.get("PORT"),
    )
