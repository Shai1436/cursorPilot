from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class StockPrice(BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    previous_close: Optional[float] = None

class StockInfo(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[int] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    eps: Optional[float] = None
    revenue: Optional[int] = None
    description: Optional[str] = None
    website: Optional[str] = None

class HistoricalData(BaseModel):
    symbol: str
    data: List[Dict[str, Any]]
    period: str

class TechnicalIndicators(BaseModel):
    symbol: str
    rsi: Optional[float] = None
    macd: Optional[Dict[str, float]] = None
    moving_averages: Optional[Dict[str, float]] = None
    bollinger_bands: Optional[Dict[str, float]] = None
    stochastic: Optional[Dict[str, float]] = None
    williams_r: Optional[float] = None
    cci: Optional[float] = None
    atr: Optional[float] = None

class FundamentalMetrics(BaseModel):
    symbol: str
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None

class StockSearchResult(BaseModel):
    symbol: str
    name: str
    type: str
    region: str
    currency: str

class TrendingStock(BaseModel):
    symbol: str
    name: str
    price: float
    change_percent: float
    volume: int