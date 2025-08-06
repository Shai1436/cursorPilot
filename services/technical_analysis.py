import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, Optional
import ta
from ta.utils import dropna
from ta.volatility import BollingerBands, AverageTrueRange
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator, CCIIndicator

class TechnicalAnalysis:
    def __init__(self):
        pass
    
    async def analyze_stock(self, symbol: str, period: str = "1y") -> Dict:
        """Perform comprehensive technical analysis"""
        try:
            # Get historical data
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            
            if df.empty:
                raise Exception(f"No data available for {symbol}")
            
            # Clean the data
            df = dropna(df)
            
            # Calculate all indicators
            indicators = {}
            
            # Moving Averages
            indicators["moving_averages"] = await self._calculate_moving_averages(df)
            
            # RSI
            indicators["rsi"] = await self._calculate_rsi(df)
            
            # MACD
            indicators["macd"] = await self._calculate_macd(df)
            
            # Bollinger Bands
            indicators["bollinger_bands"] = await self._calculate_bollinger_bands(df)
            
            # Stochastic Oscillator
            indicators["stochastic"] = await self._calculate_stochastic(df)
            
            # Williams %R
            indicators["williams_r"] = await self._calculate_williams_r(df)
            
            # CCI (Commodity Channel Index)
            indicators["cci"] = await self._calculate_cci(df)
            
            # ATR (Average True Range)
            indicators["atr"] = await self._calculate_atr(df)
            
            # Support and Resistance levels
            indicators["support_resistance"] = await self._calculate_support_resistance(df)
            
            # Trading signals
            indicators["signals"] = await self._generate_signals(df, indicators)
            
            return {
                "symbol": symbol.upper(),
                "period": period,
                "last_updated": df.index[-1].strftime("%Y-%m-%d"),
                "current_price": round(df['Close'].iloc[-1], 2),
                "indicators": indicators
            }
            
        except Exception as e:
            raise Exception(f"Technical analysis failed for {symbol}: {str(e)}")
    
    async def _calculate_moving_averages(self, df: pd.DataFrame) -> Dict:
        """Calculate various moving averages"""
        try:
            sma_20 = SMAIndicator(close=df['Close'], window=20).sma_indicator()
            sma_50 = SMAIndicator(close=df['Close'], window=50).sma_indicator()
            sma_200 = SMAIndicator(close=df['Close'], window=200).sma_indicator()
            
            ema_12 = EMAIndicator(close=df['Close'], window=12).ema_indicator()
            ema_26 = EMAIndicator(close=df['Close'], window=26).ema_indicator()
            
            current_price = df['Close'].iloc[-1]
            
            return {
                "sma_20": round(sma_20.iloc[-1], 2) if not sma_20.empty else None,
                "sma_50": round(sma_50.iloc[-1], 2) if not sma_50.empty else None,
                "sma_200": round(sma_200.iloc[-1], 2) if not sma_200.empty else None,
                "ema_12": round(ema_12.iloc[-1], 2) if not ema_12.empty else None,
                "ema_26": round(ema_26.iloc[-1], 2) if not ema_26.empty else None,
                "price_vs_sma_20": "above" if current_price > sma_20.iloc[-1] else "below",
                "price_vs_sma_50": "above" if current_price > sma_50.iloc[-1] else "below",
                "price_vs_sma_200": "above" if current_price > sma_200.iloc[-1] else "below"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_rsi(self, df: pd.DataFrame) -> Dict:
        """Calculate RSI (Relative Strength Index)"""
        try:
            rsi = RSIIndicator(close=df['Close'], window=14).rsi()
            current_rsi = rsi.iloc[-1]
            
            # RSI interpretation
            if current_rsi > 70:
                signal = "overbought"
            elif current_rsi < 30:
                signal = "oversold"
            else:
                signal = "neutral"
            
            return {
                "value": round(current_rsi, 2),
                "signal": signal,
                "interpretation": f"RSI is {signal}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_macd(self, df: pd.DataFrame) -> Dict:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            macd_indicator = MACD(close=df['Close'])
            macd_line = macd_indicator.macd()
            macd_signal = macd_indicator.macd_signal()
            macd_histogram = macd_indicator.macd_diff()
            
            current_macd = macd_line.iloc[-1]
            current_signal = macd_signal.iloc[-1]
            current_histogram = macd_histogram.iloc[-1]
            
            # MACD signal
            if current_macd > current_signal:
                signal = "bullish"
            else:
                signal = "bearish"
            
            return {
                "macd_line": round(current_macd, 4),
                "signal_line": round(current_signal, 4),
                "histogram": round(current_histogram, 4),
                "signal": signal
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_bollinger_bands(self, df: pd.DataFrame) -> Dict:
        """Calculate Bollinger Bands"""
        try:
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            
            upper_band = bb.bollinger_hband()
            lower_band = bb.bollinger_lband()
            middle_band = bb.bollinger_mavg()
            
            current_price = df['Close'].iloc[-1]
            current_upper = upper_band.iloc[-1]
            current_lower = lower_band.iloc[-1]
            current_middle = middle_band.iloc[-1]
            
            # Position relative to bands
            if current_price > current_upper:
                position = "above_upper"
            elif current_price < current_lower:
                position = "below_lower"
            else:
                position = "within_bands"
            
            return {
                "upper_band": round(current_upper, 2),
                "middle_band": round(current_middle, 2),
                "lower_band": round(current_lower, 2),
                "position": position,
                "bandwidth": round((current_upper - current_lower) / current_middle * 100, 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_stochastic(self, df: pd.DataFrame) -> Dict:
        """Calculate Stochastic Oscillator"""
        try:
            stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'])
            stoch_k = stoch.stoch()
            stoch_d = stoch.stoch_signal()
            
            current_k = stoch_k.iloc[-1]
            current_d = stoch_d.iloc[-1]
            
            # Stochastic signal
            if current_k > 80:
                signal = "overbought"
            elif current_k < 20:
                signal = "oversold"
            else:
                signal = "neutral"
            
            return {
                "k_percent": round(current_k, 2),
                "d_percent": round(current_d, 2),
                "signal": signal
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_williams_r(self, df: pd.DataFrame) -> Dict:
        """Calculate Williams %R"""
        try:
            williams_r = WilliamsRIndicator(high=df['High'], low=df['Low'], close=df['Close']).williams_r()
            current_wr = williams_r.iloc[-1]
            
            # Williams %R signal
            if current_wr > -20:
                signal = "overbought"
            elif current_wr < -80:
                signal = "oversold"
            else:
                signal = "neutral"
            
            return {
                "value": round(current_wr, 2),
                "signal": signal
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_cci(self, df: pd.DataFrame) -> Dict:
        """Calculate Commodity Channel Index"""
        try:
            cci = CCIIndicator(high=df['High'], low=df['Low'], close=df['Close']).cci()
            current_cci = cci.iloc[-1]
            
            # CCI signal
            if current_cci > 100:
                signal = "overbought"
            elif current_cci < -100:
                signal = "oversold"
            else:
                signal = "neutral"
            
            return {
                "value": round(current_cci, 2),
                "signal": signal
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_atr(self, df: pd.DataFrame) -> Dict:
        """Calculate Average True Range"""
        try:
            atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close']).average_true_range()
            current_atr = atr.iloc[-1]
            current_price = df['Close'].iloc[-1]
            
            return {
                "value": round(current_atr, 2),
                "percentage": round((current_atr / current_price) * 100, 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_support_resistance(self, df: pd.DataFrame) -> Dict:
        """Calculate support and resistance levels"""
        try:
            # Simple support/resistance based on recent highs and lows
            recent_data = df.tail(50)  # Last 50 days
            
            resistance = recent_data['High'].quantile(0.95)
            support = recent_data['Low'].quantile(0.05)
            
            return {
                "support": round(support, 2),
                "resistance": round(resistance, 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _generate_signals(self, df: pd.DataFrame, indicators: Dict) -> Dict:
        """Generate overall trading signals"""
        try:
            signals = []
            
            # RSI signals
            if indicators.get("rsi", {}).get("signal") == "oversold":
                signals.append("RSI indicates potential buy opportunity")
            elif indicators.get("rsi", {}).get("signal") == "overbought":
                signals.append("RSI indicates potential sell opportunity")
            
            # MACD signals
            if indicators.get("macd", {}).get("signal") == "bullish":
                signals.append("MACD shows bullish momentum")
            elif indicators.get("macd", {}).get("signal") == "bearish":
                signals.append("MACD shows bearish momentum")
            
            # Moving average signals
            ma_data = indicators.get("moving_averages", {})
            if ma_data.get("price_vs_sma_20") == "above" and ma_data.get("price_vs_sma_50") == "above":
                signals.append("Price above key moving averages - bullish trend")
            elif ma_data.get("price_vs_sma_20") == "below" and ma_data.get("price_vs_sma_50") == "below":
                signals.append("Price below key moving averages - bearish trend")
            
            return {
                "signals": signals,
                "overall_sentiment": "bullish" if len([s for s in signals if "bullish" in s.lower()]) > len([s for s in signals if "bearish" in s.lower()]) else "bearish"
            }
        except Exception as e:
            return {"error": str(e)}