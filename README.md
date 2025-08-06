# Stock Tracker Pro 📈

A comprehensive stock market tracking and analysis platform built with FastAPI and React. Track stock prices, analyze technical indicators, perform fundamental analysis, and monitor your investment portfolio.

## 🚀 Features

### Core Functionality
- **Real-time Stock Prices**: Get live stock price data and market information
- **Historical Data**: View historical price charts and trends
- **Stock Search**: Search for stocks by symbol or company name
- **Watchlist Management**: Create and manage your personal stock watchlist

### Technical Analysis
- **RSI (Relative Strength Index)**: Identify overbought/oversold conditions
- **MACD**: Moving Average Convergence Divergence analysis
- **Moving Averages**: SMA 20, 50, 200 and EMA 12, 26
- **Bollinger Bands**: Volatility and price level analysis
- **Stochastic Oscillator**: Momentum indicator
- **Williams %R**: Momentum oscillator
- **CCI (Commodity Channel Index)**: Trend strength indicator
- **ATR (Average True Range)**: Volatility measurement
- **Support & Resistance Levels**: Key price levels identification
- **Trading Signals**: Automated buy/sell signal generation

### Fundamental Analysis
- **Valuation Ratios**: P/E, P/B, P/S, PEG, EV/EBITDA
- **Profitability Metrics**: ROE, ROA, Gross/Operating/Net Margins
- **Liquidity Ratios**: Current, Quick, Cash ratios
- **Leverage Ratios**: Debt-to-Equity, Debt-to-Assets
- **Growth Metrics**: Revenue and Earnings growth rates
- **Efficiency Ratios**: Asset, Inventory, Receivables turnover
- **Dividend Analysis**: Yield, payout ratio, dividend growth
- **Financial Health Score**: Overall company health rating

### User Interface
- **Modern Material-UI Design**: Clean, professional interface
- **Interactive Charts**: Price charts with technical indicators
- **Real-time Updates**: WebSocket integration for live data
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme Support**: Customizable appearance
- **Advanced Search**: Autocomplete stock search functionality

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Core programming language
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database for data storage
- **yfinance**: Yahoo Finance API for stock data
- **ta (Technical Analysis)**: Technical indicators library
- **pandas & numpy**: Data manipulation and analysis
- **WebSockets**: Real-time data streaming

### Frontend
- **React 18**: Modern JavaScript library for UI
- **Material-UI (MUI)**: React component library
- **Chart.js**: Interactive charting library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API requests
- **React Hooks**: Modern state management

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock-tracker-pro
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys (optional for basic functionality)
   ```

4. **Start the backend server**
   ```bash
   ./start_backend.sh
   # Or manually: python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   npm install
   ```

2. **Start the development server**
   ```bash
   ./start_frontend.sh
   # Or manually: npm start
   ```

The frontend will be available at `http://localhost:3000`

## 🚀 Quick Start

1. **Start both servers** (backend and frontend)
2. **Open your browser** to `http://localhost:3000`
3. **Search for a stock** using the search bar in the navigation
4. **Click on a stock** to view detailed analysis
5. **Explore different tabs** for technical and fundamental analysis
6. **Add stocks to your watchlist** for easy monitoring

## 📊 API Endpoints

### Stock Data
- `GET /api/stock/{symbol}/price` - Current stock price
- `GET /api/stock/{symbol}/history` - Historical price data
- `GET /api/stock/{symbol}/info` - Company information
- `GET /api/stock/{symbol}/technical` - Technical analysis
- `GET /api/stock/{symbol}/fundamental` - Fundamental analysis

### Market Data
- `GET /api/stocks/trending` - Trending stocks
- `GET /api/stocks/search/{query}` - Search stocks
- `WebSocket /ws/{symbol}` - Real-time price updates

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
ALPHA_VANTAGE_API_KEY=your_api_key_here  # Optional

# Database Configuration
DATABASE_URL=sqlite:///./stock_tracker.db

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📱 Usage Examples

### Analyzing a Stock
1. Search for "AAPL" in the navigation bar
2. Click on Apple Inc. from the search results
3. View current price and daily metrics
4. Check the price chart for historical trends
5. Switch to "Technical Analysis" tab for trading indicators
6. Review "Fundamental Analysis" for company financials

### Creating a Watchlist
1. Navigate to the Watchlist page
2. Search and select stocks you want to track
3. Monitor price changes and performance
4. Remove stocks as needed

### Real-time Monitoring
- Stock prices update automatically
- WebSocket connections provide live data
- Charts refresh with new data points

## 🔮 Future Enhancements

- **User Authentication**: Personal accounts and portfolios
- **Advanced Charting**: More chart types and indicators
- **News Integration**: Financial news and sentiment analysis
- **Portfolio Tracking**: Investment performance monitoring
- **Alerts & Notifications**: Price and volume alerts
- **Mobile App**: Native iOS and Android applications
- **Advanced Analytics**: Machine learning predictions
- **Social Features**: Community insights and discussions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **yfinance**: For providing free stock market data
- **Yahoo Finance**: Data source for stock information
- **Material-UI**: For the beautiful React components
- **FastAPI**: For the excellent Python web framework
- **Chart.js**: For interactive charting capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](http://localhost:8000/docs) for API details
2. Search existing [issues](https://github.com/your-repo/issues)
3. Create a new issue with detailed information
4. Contact the development team

---

**Happy Trading! 📈💰**
