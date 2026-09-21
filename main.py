from fastapi import FastAPI
from api.controllers.main_router import main_router
import logging
import sys
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI()
app.include_router(main_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        port=8000
    )
