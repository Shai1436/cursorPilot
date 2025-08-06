import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime, timedelta

class FundamentalAnalysis:
    def __init__(self):
        pass
    
    async def analyze_stock(self, symbol: str) -> Dict:
        """Perform comprehensive fundamental analysis"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get financial statements
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            # Calculate fundamental metrics
            metrics = {}
            
            # Valuation ratios
            metrics["valuation"] = await self._calculate_valuation_ratios(info, financials, balance_sheet)
            
            # Profitability ratios
            metrics["profitability"] = await self._calculate_profitability_ratios(info, financials, balance_sheet)
            
            # Liquidity ratios
            metrics["liquidity"] = await self._calculate_liquidity_ratios(balance_sheet)
            
            # Leverage ratios
            metrics["leverage"] = await self._calculate_leverage_ratios(balance_sheet)
            
            # Growth metrics
            metrics["growth"] = await self._calculate_growth_metrics(financials, info)
            
            # Efficiency ratios
            metrics["efficiency"] = await self._calculate_efficiency_ratios(financials, balance_sheet)
            
            # Dividend analysis
            metrics["dividend"] = await self._analyze_dividends(info, ticker)
            
            # Company overview
            metrics["overview"] = await self._get_company_overview(info)
            
            # Financial health score
            metrics["health_score"] = await self._calculate_health_score(metrics)
            
            return {
                "symbol": symbol.upper(),
                "company_name": info.get('longName', ''),
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "metrics": metrics
            }
            
        except Exception as e:
            raise Exception(f"Fundamental analysis failed for {symbol}: {str(e)}")
    
    async def _calculate_valuation_ratios(self, info: Dict, financials: pd.DataFrame, balance_sheet: pd.DataFrame) -> Dict:
        """Calculate valuation ratios"""
        try:
            metrics = {}
            
            # P/E Ratio
            metrics["pe_ratio"] = info.get('trailingPE')
            metrics["forward_pe"] = info.get('forwardPE')
            
            # P/B Ratio
            metrics["pb_ratio"] = info.get('priceToBook')
            
            # P/S Ratio
            metrics["ps_ratio"] = info.get('priceToSalesTrailing12Months')
            
            # EV/EBITDA
            metrics["ev_ebitda"] = info.get('enterpriseToEbitda')
            
            # PEG Ratio
            metrics["peg_ratio"] = info.get('pegRatio')
            
            # Market Cap
            metrics["market_cap"] = info.get('marketCap')
            
            # Enterprise Value
            metrics["enterprise_value"] = info.get('enterpriseValue')
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_profitability_ratios(self, info: Dict, financials: pd.DataFrame, balance_sheet: pd.DataFrame) -> Dict:
        """Calculate profitability ratios"""
        try:
            metrics = {}
            
            # ROE (Return on Equity)
            metrics["roe"] = info.get('returnOnEquity')
            
            # ROA (Return on Assets)
            metrics["roa"] = info.get('returnOnAssets')
            
            # Profit Margins
            metrics["gross_margin"] = info.get('grossMargins')
            metrics["operating_margin"] = info.get('operatingMargins')
            metrics["net_margin"] = info.get('profitMargins')
            
            # EBITDA Margin
            metrics["ebitda_margin"] = info.get('ebitdaMargins')
            
            # Calculate additional margins if financial data is available
            if not financials.empty:
                try:
                    latest_financials = financials.iloc[:, 0]  # Most recent year
                    
                    total_revenue = latest_financials.get('Total Revenue')
                    gross_profit = latest_financials.get('Gross Profit')
                    operating_income = latest_financials.get('Operating Income')
                    net_income = latest_financials.get('Net Income')
                    
                    if total_revenue and total_revenue != 0:
                        if gross_profit:
                            metrics["calculated_gross_margin"] = round((gross_profit / total_revenue) * 100, 2)
                        if operating_income:
                            metrics["calculated_operating_margin"] = round((operating_income / total_revenue) * 100, 2)
                        if net_income:
                            metrics["calculated_net_margin"] = round((net_income / total_revenue) * 100, 2)
                except:
                    pass
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_liquidity_ratios(self, balance_sheet: pd.DataFrame) -> Dict:
        """Calculate liquidity ratios"""
        try:
            metrics = {}
            
            if not balance_sheet.empty:
                latest_bs = balance_sheet.iloc[:, 0]  # Most recent quarter
                
                current_assets = latest_bs.get('Current Assets')
                current_liabilities = latest_bs.get('Current Liabilities')
                cash = latest_bs.get('Cash And Cash Equivalents')
                inventory = latest_bs.get('Inventory')
                
                # Current Ratio
                if current_assets and current_liabilities and current_liabilities != 0:
                    metrics["current_ratio"] = round(current_assets / current_liabilities, 2)
                
                # Quick Ratio (Acid Test)
                if current_assets and inventory and current_liabilities and current_liabilities != 0:
                    quick_assets = current_assets - (inventory or 0)
                    metrics["quick_ratio"] = round(quick_assets / current_liabilities, 2)
                
                # Cash Ratio
                if cash and current_liabilities and current_liabilities != 0:
                    metrics["cash_ratio"] = round(cash / current_liabilities, 2)
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_leverage_ratios(self, balance_sheet: pd.DataFrame) -> Dict:
        """Calculate leverage/debt ratios"""
        try:
            metrics = {}
            
            if not balance_sheet.empty:
                latest_bs = balance_sheet.iloc[:, 0]  # Most recent quarter
                
                total_debt = latest_bs.get('Total Debt')
                total_equity = latest_bs.get('Total Equity Gross Minority Interest')
                total_assets = latest_bs.get('Total Assets')
                
                # Debt-to-Equity Ratio
                if total_debt and total_equity and total_equity != 0:
                    metrics["debt_to_equity"] = round(total_debt / total_equity, 2)
                
                # Debt-to-Assets Ratio
                if total_debt and total_assets and total_assets != 0:
                    metrics["debt_to_assets"] = round(total_debt / total_assets, 2)
                
                # Equity Ratio
                if total_equity and total_assets and total_assets != 0:
                    metrics["equity_ratio"] = round(total_equity / total_assets, 2)
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_growth_metrics(self, financials: pd.DataFrame, info: Dict) -> Dict:
        """Calculate growth metrics"""
        try:
            metrics = {}
            
            # Growth rates from info
            metrics["revenue_growth"] = info.get('revenueGrowth')
            metrics["earnings_growth"] = info.get('earningsGrowth')
            
            # Calculate historical growth if financial data is available
            if not financials.empty and len(financials.columns) >= 2:
                try:
                    current_revenue = financials.iloc[:, 0].get('Total Revenue')
                    previous_revenue = financials.iloc[:, 1].get('Total Revenue')
                    
                    if current_revenue and previous_revenue and previous_revenue != 0:
                        calculated_revenue_growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
                        metrics["calculated_revenue_growth"] = round(calculated_revenue_growth, 2)
                    
                    current_net_income = financials.iloc[:, 0].get('Net Income')
                    previous_net_income = financials.iloc[:, 1].get('Net Income')
                    
                    if current_net_income and previous_net_income and previous_net_income != 0:
                        calculated_earnings_growth = ((current_net_income - previous_net_income) / previous_net_income) * 100
                        metrics["calculated_earnings_growth"] = round(calculated_earnings_growth, 2)
                except:
                    pass
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_efficiency_ratios(self, financials: pd.DataFrame, balance_sheet: pd.DataFrame) -> Dict:
        """Calculate efficiency ratios"""
        try:
            metrics = {}
            
            if not financials.empty and not balance_sheet.empty:
                latest_financials = financials.iloc[:, 0]
                latest_bs = balance_sheet.iloc[:, 0]
                
                total_revenue = latest_financials.get('Total Revenue')
                total_assets = latest_bs.get('Total Assets')
                inventory = latest_bs.get('Inventory')
                accounts_receivable = latest_bs.get('Accounts Receivable')
                
                # Asset Turnover
                if total_revenue and total_assets and total_assets != 0:
                    metrics["asset_turnover"] = round(total_revenue / total_assets, 2)
                
                # Inventory Turnover (using revenue as proxy for COGS)
                if total_revenue and inventory and inventory != 0:
                    metrics["inventory_turnover"] = round(total_revenue / inventory, 2)
                
                # Receivables Turnover
                if total_revenue and accounts_receivable and accounts_receivable != 0:
                    metrics["receivables_turnover"] = round(total_revenue / accounts_receivable, 2)
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _analyze_dividends(self, info: Dict, ticker) -> Dict:
        """Analyze dividend information"""
        try:
            metrics = {}
            
            # Basic dividend info
            metrics["dividend_yield"] = info.get('dividendYield')
            metrics["dividend_rate"] = info.get('dividendRate')
            metrics["payout_ratio"] = info.get('payoutRatio')
            
            # Dividend dates
            metrics["ex_dividend_date"] = info.get('exDividendDate')
            metrics["dividend_date"] = info.get('dividendDate')
            
            # Try to get dividend history
            try:
                dividends = ticker.dividends
                if not dividends.empty:
                    recent_dividends = dividends.tail(4)  # Last 4 dividends
                    metrics["recent_dividends"] = recent_dividends.tolist()
                    
                    # Calculate dividend growth
                    if len(recent_dividends) >= 2:
                        latest_dividend = recent_dividends.iloc[-1]
                        previous_dividend = recent_dividends.iloc[-2]
                        if previous_dividend != 0:
                            dividend_growth = ((latest_dividend - previous_dividend) / previous_dividend) * 100
                            metrics["dividend_growth"] = round(dividend_growth, 2)
            except:
                pass
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_company_overview(self, info: Dict) -> Dict:
        """Get company overview information"""
        try:
            return {
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "employees": info.get('fullTimeEmployees'),
                "country": info.get('country'),
                "website": info.get('website'),
                "business_summary": info.get('longBusinessSummary', '')[:500] + '...' if info.get('longBusinessSummary') and len(info.get('longBusinessSummary', '')) > 500 else info.get('longBusinessSummary', ''),
                "founded": info.get('yearFounded')
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _calculate_health_score(self, metrics: Dict) -> Dict:
        """Calculate overall financial health score"""
        try:
            score = 0
            max_score = 0
            
            # Profitability (30 points)
            profitability = metrics.get('profitability', {})
            if profitability.get('roe') and profitability['roe'] > 0.15:
                score += 10
            max_score += 10
            
            if profitability.get('net_margin') and profitability['net_margin'] > 0.1:
                score += 10
            max_score += 10
            
            if profitability.get('operating_margin') and profitability['operating_margin'] > 0.15:
                score += 10
            max_score += 10
            
            # Liquidity (20 points)
            liquidity = metrics.get('liquidity', {})
            if liquidity.get('current_ratio') and liquidity['current_ratio'] > 1.5:
                score += 10
            max_score += 10
            
            if liquidity.get('quick_ratio') and liquidity['quick_ratio'] > 1.0:
                score += 10
            max_score += 10
            
            # Leverage (20 points)
            leverage = metrics.get('leverage', {})
            if leverage.get('debt_to_equity') and leverage['debt_to_equity'] < 0.5:
                score += 20
            elif leverage.get('debt_to_equity') and leverage['debt_to_equity'] < 1.0:
                score += 10
            max_score += 20
            
            # Growth (20 points)
            growth = metrics.get('growth', {})
            if growth.get('revenue_growth') and growth['revenue_growth'] > 0.1:
                score += 10
            max_score += 10
            
            if growth.get('earnings_growth') and growth['earnings_growth'] > 0.1:
                score += 10
            max_score += 10
            
            # Valuation (10 points)
            valuation = metrics.get('valuation', {})
            if valuation.get('pe_ratio') and 10 <= valuation['pe_ratio'] <= 20:
                score += 10
            max_score += 10
            
            final_score = (score / max_score * 100) if max_score > 0 else 0
            
            # Determine rating
            if final_score >= 80:
                rating = "Excellent"
            elif final_score >= 60:
                rating = "Good"
            elif final_score >= 40:
                rating = "Fair"
            else:
                rating = "Poor"
            
            return {
                "score": round(final_score, 1),
                "rating": rating,
                "max_score": 100
            }
        except Exception as e:
            return {"error": str(e)}