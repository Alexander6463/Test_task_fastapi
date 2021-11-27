import os

from fastapi import FastAPI
from src.users import router
from src.log import configure_logging
import uvicorn

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    logger = configure_logging(os.environ.get("LOG_FILE_PATH"))
    uvicorn.run(
        "main:app",
        host=os.environ.get("APP_HOST"),
        port=int(os.environ.get("APP_PORT")),
    )
