
from fastapi import FastAPI
from api.router import api_router
import logging
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EDR_Central")

app = FastAPI(title="EDR `Pipeline`")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "127.0.0.1",
        port = 8000,
        reload = True
    )

app.include_router(api_router)

# Run with: main.py