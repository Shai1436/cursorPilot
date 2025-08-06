import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Button,
  IconButton,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
} from '@mui/icons-material';

const Watchlist = () => {
  const navigate = useNavigate();
  const [watchlist, setWatchlist] = useState([]);

  // Mock watchlist data - in a real app, this would come from backend/localStorage
  useEffect(() => {
    const mockWatchlist = [
      { symbol: 'AAPL', name: 'Apple Inc.', price: 150.25, change: 2.45, change_percent: 1.66 },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2750.80, change: -15.20, change_percent: -0.55 },
      { symbol: 'TSLA', name: 'Tesla Inc.', price: 245.60, change: 8.90, change_percent: 3.76 },
    ];
    setWatchlist(mockWatchlist);
  }, []);

  const removeFromWatchlist = (symbol) => {
    setWatchlist(prev => prev.filter(stock => stock.symbol !== symbol));
  };

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Watchlist
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Track your favorite stocks and monitor their performance
        </Typography>
      </Box>

      {watchlist.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" gutterBottom>
              Your watchlist is empty
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Start by searching for stocks and adding them to your watchlist
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/')}
            >
              Explore Stocks
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {watchlist.map((stock) => (
            <Grid item xs={12} sm={6} md={4} key={stock.symbol}>
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
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                    <Box>
                      <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
                        {stock.symbol}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" noWrap>
                        {stock.name}
                      </Typography>
                    </Box>
                    <IconButton
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFromWatchlist(stock.symbol);
                      }}
                      sx={{ color: 'error.main' }}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Box>

                  <Box>
                    <Typography variant="h6" component="div">
                      ${stock.price.toFixed(2)}
                    </Typography>
                    <Box display="flex" alignItems="center">
                      {stock.change >= 0 ? (
                        <TrendingUpIcon color="success" fontSize="small" />
                      ) : (
                        <TrendingDownIcon color="error" fontSize="small" />
                      )}
                      <Typography
                        variant="body2"
                        color={stock.change >= 0 ? 'success.main' : 'error.main'}
                        sx={{ ml: 0.5 }}
                      >
                        {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)} ({stock.change_percent.toFixed(2)}%)
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Watchlist;