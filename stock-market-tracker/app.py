from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from services.alphavantage import get_stock_data
import os
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/api/stocks/{symbol}")
async def get_stock(symbol: str):
    try:
        data = get_stock_data(symbol)
        return data
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/static/{filename}")
async def static_files(filename: str):
    return FileResponse(f"static/{filename}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)