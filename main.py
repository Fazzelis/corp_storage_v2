from fastapi import FastAPI
from api.controllers.main_router import main_router
import logging
import sys
from api.exceptions.reg_exseptions import registrate_all_exceptions

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI()
app.include_router(main_router)
registrate_all_exceptions(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        port=8000
    )
