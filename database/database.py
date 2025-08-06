from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sqlite3
import os

DATABASE_URL = "sqlite:///./stock_tracker.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class StockPriceDB(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    change = Column(Float)
    change_percent = Column(Float)
    volume = Column(Integer)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    previous_close = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class StockInfoDB(Base):
    __tablename__ = "stock_info"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    company_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Integer)
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    beta = Column(Float)
    eps = Column(Float)
    revenue = Column(Integer)
    description = Column(Text)
    website = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

class WatchlistDB(Base):
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # For future user management
    symbol = Column(String, index=True)
    added_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class AlertDB(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    symbol = Column(String, index=True)
    alert_type = Column(String)  # 'price_above', 'price_below', 'volume_spike'
    target_value = Column(Float)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    triggered_date = Column(DateTime, nullable=True)

async def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()