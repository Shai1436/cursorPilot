from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import yfinance as yf
import pandas as pd
from pydantic import BaseModel
from services.stock_service import StockService
from services.technical_analysis import TechnicalAnalysis
from services.fundamental_analysis import FundamentalAnalysis
from database.database import init_db, get_db
from models.stock_models import StockPrice, StockInfo
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
stock_service = StockService()
technical_analysis = TechnicalAnalysis()
fundamental_analysis = FundamentalAnalysis()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Pydantic models
class StockRequest(BaseModel):
    symbol: str

class StockAnalysisRequest(BaseModel):
    symbol: str
    period: str = "1y"

# API Routes
@app.get("/")
async def root():
    return {"message": "Stock Tracker API is running"}

@app.get("/api/stock/{symbol}/price")
async def get_current_price(symbol: str):
    """Get current stock price"""
    try:
        price_data = await stock_service.get_current_price(symbol)
        return price_data
    except Exception as e:
        logger.error(f"Error getting price for {symbol}: {e}")
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

@app.get("/api/stock/{symbol}/history")
async def get_stock_history(symbol: str, period: str = "1y"):
    """Get historical stock data"""
    try:
        history = await stock_service.get_historical_data(symbol, period)
        return history
    except Exception as e:
        logger.error(f"Error getting history for {symbol}: {e}")
        raise HTTPException(status_code=404, detail=f"Historical data for {symbol} not found")

@app.get("/api/stock/{symbol}/info")
async def get_stock_info(symbol: str):
    """Get stock company information"""
    try:
        info = await stock_service.get_stock_info(symbol)
        return info
    except Exception as e:
        logger.error(f"Error getting info for {symbol}: {e}")
        raise HTTPException(status_code=404, detail=f"Stock info for {symbol} not found")

@app.get("/api/stock/{symbol}/technical")
async def get_technical_analysis(symbol: str, period: str = "1y"):
    """Get technical analysis indicators"""
    try:
        analysis = await technical_analysis.analyze_stock(symbol, period)
        return analysis
    except Exception as e:
        logger.error(f"Error getting technical analysis for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Technical analysis failed")

@app.get("/api/stock/{symbol}/fundamental")
async def get_fundamental_analysis(symbol: str):
    """Get fundamental analysis data"""
    try:
        analysis = await fundamental_analysis.analyze_stock(symbol)
        return analysis
    except Exception as e:
        logger.error(f"Error getting fundamental analysis for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Fundamental analysis failed")

@app.get("/api/stocks/trending")
async def get_trending_stocks():
    """Get trending stocks"""
    try:
        trending = await stock_service.get_trending_stocks()
        return trending
    except Exception as e:
        logger.error(f"Error getting trending stocks: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trending stocks")

@app.get("/api/stocks/search/{query}")
async def search_stocks(query: str):
    """Search for stocks by symbol or company name"""
    try:
        results = await stock_service.search_stocks(query)
        return results
    except Exception as e:
        logger.error(f"Error searching stocks: {e}")
        raise HTTPException(status_code=500, detail="Stock search failed")

@app.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """WebSocket endpoint for real-time stock updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Get current price
            price_data = await stock_service.get_current_price(symbol)
            await manager.send_personal_message(json.dumps(price_data), websocket)
            await asyncio.sleep(5)  # Update every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Background task for periodic updates
async def periodic_updates():
    """Background task to update stock data periodically"""
    while True:
        try:
            # Update trending stocks every 30 minutes
            await asyncio.sleep(1800)
            logger.info("Updating trending stocks...")
        except Exception as e:
            logger.error(f"Error in periodic updates: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    await init_db()
    # Start background task
    asyncio.create_task(periodic_updates())
    logger.info("Stock Tracker API started successfully")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)