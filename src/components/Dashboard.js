import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Chip,
  IconButton,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Visibility as VisibilityIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [trendingStocks, setTrendingStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTrendingStocks();
  }, []);

  const fetchTrendingStocks = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/stocks/trending');
      setTrendingStocks(response.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching trending stocks:', error);
      setError('Failed to load trending stocks');
    } finally {
      setLoading(false);
    }
  };

  const formatMarketCap = (marketCap) => {
    if (!marketCap) return 'N/A';
    
    if (marketCap >= 1e12) {
      return `$${(marketCap / 1e12).toFixed(1)}T`;
    } else if (marketCap >= 1e9) {
      return `$${(marketCap / 1e9).toFixed(1)}B`;
    } else if (marketCap >= 1e6) {
      return `$${(marketCap / 1e6).toFixed(1)}M`;
    }
    return `$${marketCap}`;
  };

  const formatVolume = (volume) => {
    if (!volume) return 'N/A';
    
    if (volume >= 1e9) {
      return `${(volume / 1e9).toFixed(1)}B`;
    } else if (volume >= 1e6) {
      return `${(volume / 1e6).toFixed(1)}M`;
    } else if (volume >= 1e3) {
      return `${(volume / 1e3).toFixed(1)}K`;
    }
    return volume.toString();
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

  return (
    <Container maxWidth="lg">
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Stock Market Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Track your investments and discover trending stocks
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Market Overview Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Market Status
              </Typography>
              <Typography variant="h5" component="div">
                <Chip 
                  label="Open" 
                  color="success" 
                  size="small"
                  icon={<TrendingUpIcon />}
                />
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Trending Stocks
              </Typography>
              <Typography variant="h5" component="div">
                {trendingStocks.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Active Alerts
              </Typography>
              <Typography variant="h5" component="div">
                0
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Watchlist Items
              </Typography>
              <Typography variant="h5" component="div">
                0
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Trending Stocks */}
      <Box mb={4}>
        <Typography variant="h5" component="h2" gutterBottom>
          Trending Stocks
        </Typography>
        <Grid container spacing={2}>
          {trendingStocks.map((stock) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={stock.symbol}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: 4,
                  }
                }}
                onClick={() => navigate(`/stock/${stock.symbol}`)}
              >
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                    <Box>
                      <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
                        {stock.symbol}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" noWrap>
                        {stock.name}
                      </Typography>
                    </Box>
                    <IconButton size="small" onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/stock/${stock.symbol}`);
                    }}>
                      <VisibilityIcon fontSize="small" />
                    </IconButton>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="h6" component="div">
                      ${stock.price?.toFixed(2) || 'N/A'}
                    </Typography>
                    <Box display="flex" alignItems="center">
                      {stock.change_percent > 0 ? (
                        <TrendingUpIcon color="success" fontSize="small" />
                      ) : (
                        <TrendingDownIcon color="error" fontSize="small" />
                      )}
                      <Typography
                        variant="body2"
                        color={stock.change_percent > 0 ? 'success.main' : 'error.main'}
                        sx={{ ml: 0.5 }}
                      >
                        {stock.change_percent > 0 ? '+' : ''}{stock.change_percent?.toFixed(2) || '0.00'}%
                      </Typography>
                    </Box>
                  </Box>

                  <Box>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Volume: {formatVolume(stock.volume)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Market Cap: {formatMarketCap(stock.market_cap)}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Quick Actions */}
      <Box>
        <Typography variant="h5" component="h2" gutterBottom>
          Quick Actions
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={4}>
            <Card 
              sx={{ 
                cursor: 'pointer',
                textAlign: 'center',
                py: 3,
                '&:hover': {
                  backgroundColor: 'action.hover',
                }
              }}
              onClick={() => navigate('/market')}
            >
              <CardContent>
                <TrendingUpIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h6" component="div">
                  Explore Market
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Browse all available stocks
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card 
              sx={{ 
                cursor: 'pointer',
                textAlign: 'center',
                py: 3,
                '&:hover': {
                  backgroundColor: 'action.hover',
                }
              }}
              onClick={() => navigate('/watchlist')}
            >
              <CardContent>
                <AddIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h6" component="div">
                  Create Watchlist
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Track your favorite stocks
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;