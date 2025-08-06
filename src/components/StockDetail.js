import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Chip,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Divider,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Business as BusinessIcon,
  Analytics as AnalyticsIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StockDetail = () => {
  const { symbol } = useParams();
  const [stockData, setStockData] = useState(null);
  const [stockInfo, setStockInfo] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [technicalAnalysis, setTechnicalAnalysis] = useState(null);
  const [fundamentalAnalysis, setFundamentalAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    if (symbol) {
      fetchStockData();
    }
  }, [symbol]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all stock data in parallel
      const [priceRes, infoRes, historyRes, technicalRes, fundamentalRes] = await Promise.allSettled([
        axios.get(`/api/stock/${symbol}/price`),
        axios.get(`/api/stock/${symbol}/info`),
        axios.get(`/api/stock/${symbol}/history?period=1y`),
        axios.get(`/api/stock/${symbol}/technical`),
        axios.get(`/api/stock/${symbol}/fundamental`),
      ]);

      if (priceRes.status === 'fulfilled') setStockData(priceRes.value.data);
      if (infoRes.status === 'fulfilled') setStockInfo(infoRes.value.data);
      if (historyRes.status === 'fulfilled') setHistoricalData(historyRes.value.data);
      if (technicalRes.status === 'fulfilled') setTechnicalAnalysis(technicalRes.value.data);
      if (fundamentalRes.status === 'fulfilled') setFundamentalAnalysis(fundamentalRes.value.data);

    } catch (error) {
      console.error('Error fetching stock data:', error);
      setError('Failed to load stock data');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num, decimals = 2) => {
    if (num === null || num === undefined) return 'N/A';
    return typeof num === 'number' ? num.toFixed(decimals) : num;
  };

  const formatLargeNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return `$${(num / 1e12).toFixed(1)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(1)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(1)}M`;
    return `$${num.toLocaleString()}`;
  };

  const createChartData = () => {
    if (!historicalData || !historicalData.data) return null;

    const data = historicalData.data.slice(-90); // Last 90 days
    
    return {
      labels: data.map(item => new Date(item.date).toLocaleDateString()),
      datasets: [
        {
          label: 'Close Price',
          data: data.map(item => item.close),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.1)',
          tension: 0.1,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${symbol} - Price Chart (Last 90 Days)`,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  const TabPanel = ({ children, value, index }) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Container maxWidth="lg">
      {/* Header */}
      {stockData && (
        <Box mb={4}>
          <Typography variant="h4" component="h1" gutterBottom>
            {symbol}
          </Typography>
          {stockInfo && (
            <Typography variant="h6" color="text.secondary" gutterBottom>
              {stockInfo.company_name}
            </Typography>
          )}
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="h5" component="span">
              ${formatNumber(stockData.price)}
            </Typography>
            <Chip
              icon={stockData.change >= 0 ? <TrendingUpIcon /> : <TrendingDownIcon />}
              label={`${stockData.change >= 0 ? '+' : ''}${formatNumber(stockData.change)} (${formatNumber(stockData.change_percent)}%)`}
              color={stockData.change >= 0 ? 'success' : 'error'}
            />
          </Box>
        </Box>
      )}

      {/* Key Metrics */}
      {stockData && (
        <Grid container spacing={3} mb={4}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Open
                </Typography>
                <Typography variant="h6">
                  ${formatNumber(stockData.open)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  High
                </Typography>
                <Typography variant="h6">
                  ${formatNumber(stockData.high)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Low
                </Typography>
                <Typography variant="h6">
                  ${formatNumber(stockData.low)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Volume
                </Typography>
                <Typography variant="h6">
                  {stockData.volume?.toLocaleString() || 'N/A'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Chart */}
      {historicalData && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Line data={createChartData()} options={chartOptions} />
          </CardContent>
        </Card>
      )}

      {/* Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab icon={<BusinessIcon />} label="Company Info" />
            <Tab icon={<AnalyticsIcon />} label="Technical Analysis" />
            <Tab icon={<AssessmentIcon />} label="Fundamental Analysis" />
          </Tabs>
        </Box>

        {/* Company Info Tab */}
        <TabPanel value={activeTab} index={0}>
          {stockInfo ? (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Company Overview
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableBody>
                      <TableRow>
                        <TableCell><strong>Sector</strong></TableCell>
                        <TableCell>{stockInfo.sector || 'N/A'}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>Industry</strong></TableCell>
                        <TableCell>{stockInfo.industry || 'N/A'}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>Market Cap</strong></TableCell>
                        <TableCell>{formatLargeNumber(stockInfo.market_cap)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>P/E Ratio</strong></TableCell>
                        <TableCell>{formatNumber(stockInfo.pe_ratio)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>Beta</strong></TableCell>
                        <TableCell>{formatNumber(stockInfo.beta)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>Dividend Yield</strong></TableCell>
                        <TableCell>{stockInfo.dividend_yield ? `${(stockInfo.dividend_yield * 100).toFixed(2)}%` : 'N/A'}</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Company Details
                </Typography>
                <Box>
                  <Typography variant="body2" paragraph>
                    <strong>Employees:</strong> {stockInfo.employees?.toLocaleString() || 'N/A'}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Headquarters:</strong> {stockInfo.headquarters || 'N/A'}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Website:</strong> {stockInfo.website ? (
                      <a href={stockInfo.website} target="_blank" rel="noopener noreferrer">
                        {stockInfo.website}
                      </a>
                    ) : 'N/A'}
                  </Typography>
                  {stockInfo.description && (
                    <>
                      <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                        Description
                      </Typography>
                      <Typography variant="body2">
                        {stockInfo.description}
                      </Typography>
                    </>
                  )}
                </Box>
              </Grid>
            </Grid>
          ) : (
            <Typography>No company information available</Typography>
          )}
        </TabPanel>

        {/* Technical Analysis Tab */}
        <TabPanel value={activeTab} index={1}>
          {technicalAnalysis ? (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Technical Indicators
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableBody>
                      {technicalAnalysis.indicators?.rsi && (
                        <TableRow>
                          <TableCell><strong>RSI (14)</strong></TableCell>
                          <TableCell>
                            <Chip 
                              label={`${technicalAnalysis.indicators.rsi.value} (${technicalAnalysis.indicators.rsi.signal})`}
                              color={
                                technicalAnalysis.indicators.rsi.signal === 'overbought' ? 'error' :
                                technicalAnalysis.indicators.rsi.signal === 'oversold' ? 'success' : 'default'
                              }
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      )}
                      {technicalAnalysis.indicators?.macd && (
                        <TableRow>
                          <TableCell><strong>MACD</strong></TableCell>
                          <TableCell>
                            <Chip 
                              label={technicalAnalysis.indicators.macd.signal}
                              color={technicalAnalysis.indicators.macd.signal === 'bullish' ? 'success' : 'error'}
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      )}
                      {technicalAnalysis.indicators?.moving_averages && (
                        <>
                          <TableRow>
                            <TableCell><strong>SMA 20</strong></TableCell>
                            <TableCell>${technicalAnalysis.indicators.moving_averages.sma_20}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell><strong>SMA 50</strong></TableCell>
                            <TableCell>${technicalAnalysis.indicators.moving_averages.sma_50}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell><strong>SMA 200</strong></TableCell>
                            <TableCell>${technicalAnalysis.indicators.moving_averages.sma_200}</TableCell>
                          </TableRow>
                        </>
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Trading Signals
                </Typography>
                {technicalAnalysis.indicators?.signals?.signals && (
                  <Box>
                    {technicalAnalysis.indicators.signals.signals.map((signal, index) => (
                      <Chip
                        key={index}
                        label={signal}
                        variant="outlined"
                        sx={{ mr: 1, mb: 1 }}
                      />
                    ))}
                  </Box>
                )}
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    <strong>Overall Sentiment:</strong> {' '}
                    <Chip
                      label={technicalAnalysis.indicators?.signals?.overall_sentiment || 'Neutral'}
                      color={
                        technicalAnalysis.indicators?.signals?.overall_sentiment === 'bullish' ? 'success' : 'error'
                      }
                      size="small"
                    />
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          ) : (
            <Typography>No technical analysis available</Typography>
          )}
        </TabPanel>

        {/* Fundamental Analysis Tab */}
        <TabPanel value={activeTab} index={2}>
          {fundamentalAnalysis ? (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Valuation Ratios
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableBody>
                      <TableRow>
                        <TableCell><strong>P/E Ratio</strong></TableCell>
                        <TableCell>{formatNumber(fundamentalAnalysis.metrics?.valuation?.pe_ratio)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>P/B Ratio</strong></TableCell>
                        <TableCell>{formatNumber(fundamentalAnalysis.metrics?.valuation?.pb_ratio)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>P/S Ratio</strong></TableCell>
                        <TableCell>{formatNumber(fundamentalAnalysis.metrics?.valuation?.ps_ratio)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>PEG Ratio</strong></TableCell>
                        <TableCell>{formatNumber(fundamentalAnalysis.metrics?.valuation?.peg_ratio)}</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                  Financial Health
                </Typography>
                {fundamentalAnalysis.metrics?.health_score && (
                  <Box>
                    <Typography variant="body2">
                      <strong>Health Score:</strong> {fundamentalAnalysis.metrics.health_score.score}/100
                    </Typography>
                    <Chip
                      label={fundamentalAnalysis.metrics.health_score.rating}
                      color={
                        fundamentalAnalysis.metrics.health_score.rating === 'Excellent' ? 'success' :
                        fundamentalAnalysis.metrics.health_score.rating === 'Good' ? 'primary' :
                        fundamentalAnalysis.metrics.health_score.rating === 'Fair' ? 'warning' : 'error'
                      }
                      sx={{ mt: 1 }}
                    />
                  </Box>
                )}
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Profitability
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableBody>
                      <TableRow>
                        <TableCell><strong>ROE</strong></TableCell>
                        <TableCell>
                          {fundamentalAnalysis.metrics?.profitability?.roe 
                            ? `${(fundamentalAnalysis.metrics.profitability.roe * 100).toFixed(2)}%`
                            : 'N/A'}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>ROA</strong></TableCell>
                        <TableCell>
                          {fundamentalAnalysis.metrics?.profitability?.roa 
                            ? `${(fundamentalAnalysis.metrics.profitability.roa * 100).toFixed(2)}%`
                            : 'N/A'}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>Gross Margin</strong></TableCell>
                        <TableCell>
                          {fundamentalAnalysis.metrics?.profitability?.gross_margin 
                            ? `${(fundamentalAnalysis.metrics.profitability.gross_margin * 100).toFixed(2)}%`
                            : 'N/A'}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell><strong>Net Margin</strong></TableCell>
                        <TableCell>
                          {fundamentalAnalysis.metrics?.profitability?.net_margin 
                            ? `${(fundamentalAnalysis.metrics.profitability.net_margin * 100).toFixed(2)}%`
                            : 'N/A'}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
            </Grid>
          ) : (
            <Typography>No fundamental analysis available</Typography>
          )}
        </TabPanel>
      </Card>
    </Container>
  );
};

export default StockDetail;