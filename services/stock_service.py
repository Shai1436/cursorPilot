import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import aiohttp
import json
from models.stock_models import StockPrice, StockInfo, HistoricalData, TrendingStock, StockSearchResult

class StockService:
    def __init__(self):
        self.trending_symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "AMD", "INTC"
        ]
    
    async def get_current_price(self, symbol: str) -> Dict:
        """Get current stock price and basic info"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price data
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
            
            if current_price is None:
                # Fallback to recent data
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            
            change = current_price - previous_close if previous_close else 0
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            return {
                "symbol": symbol.upper(),
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "volume": info.get('volume', 0),
                "high": info.get('dayHigh'),
                "low": info.get('dayLow'),
                "open": info.get('open'),
                "previous_close": previous_close,
                "timestamp": datetime.now()
            }
        except Exception as e:
            raise Exception(f"Error fetching price data for {symbol}: {str(e)}")
    
    async def get_historical_data(self, symbol: str, period: str = "1y") -> Dict:
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise Exception(f"No historical data found for {symbol}")
            
            # Convert to list of dictionaries
            data = []
            for index, row in hist.iterrows():
                data.append({
                    "date": index.strftime("%Y-%m-%d"),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2),
                    "volume": int(row['Volume'])
                })
            
            return {
                "symbol": symbol.upper(),
                "period": period,
                "data": data
            }
        except Exception as e:
            raise Exception(f"Error fetching historical data for {symbol}: {str(e)}")
    
    async def get_stock_info(self, symbol: str) -> Dict:
        """Get detailed stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol.upper(),
                "company_name": info.get('longName', ''),
                "sector": info.get('sector', ''),
                "industry": info.get('industry', ''),
                "market_cap": info.get('marketCap'),
                "pe_ratio": info.get('trailingPE'),
                "dividend_yield": info.get('dividendYield'),
                "beta": info.get('beta'),
                "eps": info.get('trailingEps'),
                "revenue": info.get('totalRevenue'),
                "description": info.get('longBusinessSummary', ''),
                "website": info.get('website', ''),
                "employees": info.get('fullTimeEmployees'),
                "headquarters": f"{info.get('city', '')}, {info.get('state', '')} {info.get('country', '')}".strip(', '),
                "founded": info.get('yearFounded'),
                "ceo": info.get('companyOfficers', [{}])[0].get('name') if info.get('companyOfficers') else None
            }
        except Exception as e:
            raise Exception(f"Error fetching stock info for {symbol}: {str(e)}")
    
    async def get_trending_stocks(self) -> List[Dict]:
        """Get trending stocks data"""
        try:
            trending_data = []
            
            for symbol in self.trending_symbols:
                try:
                    price_data = await self.get_current_price(symbol)
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    trending_data.append({
                        "symbol": symbol,
                        "name": info.get('shortName', symbol),
                        "price": price_data["price"],
                        "change_percent": price_data["change_percent"],
                        "volume": price_data["volume"],
                        "market_cap": info.get('marketCap')
                    })
                except:
                    continue
            
            # Sort by absolute change percentage (most volatile first)
            trending_data.sort(key=lambda x: abs(x["change_percent"]), reverse=True)
            return trending_data[:10]
            
        except Exception as e:
            raise Exception(f"Error fetching trending stocks: {str(e)}")
    
    async def search_stocks(self, query: str) -> List[Dict]:
        """Search for stocks by symbol or company name"""
        try:
            # Common stocks dictionary for quick lookup
            common_stocks = {
                "AAPL": "Apple Inc.",
                "MSFT": "Microsoft Corporation",
                "GOOGL": "Alphabet Inc.",
                "AMZN": "Amazon.com Inc.",
                "TSLA": "Tesla Inc.",
                "META": "Meta Platforms Inc.",
                "NVDA": "NVIDIA Corporation",
                "NFLX": "Netflix Inc.",
                "AMD": "Advanced Micro Devices Inc.",
                "INTC": "Intel Corporation",
                "JPM": "JPMorgan Chase & Co.",
                "V": "Visa Inc.",
                "JNJ": "Johnson & Johnson",
                "WMT": "Walmart Inc.",
                "PG": "Procter & Gamble Co.",
                "UNH": "UnitedHealth Group Inc.",
                "DIS": "Walt Disney Co.",
                "HD": "Home Depot Inc.",
                "MA": "Mastercard Inc.",
                "BAC": "Bank of America Corp."
            }
            
            results = []
            query_upper = query.upper()
            
            # Search by symbol
            for symbol, name in common_stocks.items():
                if query_upper in symbol or query_upper.lower() in name.lower():
                    results.append({
                        "symbol": symbol,
                        "name": name,
                        "type": "Common Stock",
                        "region": "US",
                        "currency": "USD"
                    })
            
            # If exact symbol match, try to get real data
            if query_upper in common_stocks or len(query_upper) <= 5:
                try:
                    ticker = yf.Ticker(query_upper)
                    info = ticker.info
                    if info.get('symbol'):
                        results.insert(0, {
                            "symbol": info.get('symbol', query_upper),
                            "name": info.get('longName', info.get('shortName', query)),
                            "type": "Common Stock",
                            "region": "US",
                            "currency": "USD"
                        })
                except:
                    pass
            
            return results[:10]  # Limit to 10 results
            
        except Exception as e:
            raise Exception(f"Error searching stocks: {str(e)}")
    
    async def get_market_status(self) -> Dict:
        """Get market status and trading hours"""
        try:
            # Simple market status based on time (US Eastern Time)
            now = datetime.now()
            
            # Market hours: 9:30 AM - 4:00 PM ET (weekdays)
            market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
            market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
            
            is_weekend = now.weekday() >= 5  # Saturday = 5, Sunday = 6
            is_market_hours = market_open <= now <= market_close and not is_weekend
            
            return {
                "is_open": is_market_hours,
                "next_open": market_open.isoformat() if not is_market_hours else None,
                "next_close": market_close.isoformat() if is_market_hours else None,
                "timezone": "US/Eastern"
            }
        except Exception as e:
            return {"is_open": False, "error": str(e)}