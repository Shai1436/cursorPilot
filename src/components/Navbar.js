import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  TextField,
  InputAdornment,
  IconButton,
  Menu,
  MenuItem,
  Autocomplete,
} from '@mui/material';
import {
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  Dashboard as DashboardIcon,
  Bookmark as BookmarkIcon,
  ShowChart as ShowChartIcon,
} from '@mui/icons-material';
import axios from 'axios';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);

  const handleSearch = async (query) => {
    if (!query || query.length < 1) {
      setSearchResults([]);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await axios.get(`/api/stocks/search/${query}`);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleStockSelect = (stock) => {
    if (stock) {
      navigate(`/stock/${stock.symbol}`);
      setSearchQuery('');
      setSearchResults([]);
    }
  };

  const navigationItems = [
    { label: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    { label: 'Market', path: '/market', icon: <TrendingUpIcon /> },
    { label: 'Watchlist', path: '/watchlist', icon: <BookmarkIcon /> },
  ];

  return (
    <AppBar position="sticky" elevation={1}>
      <Toolbar>
        {/* Logo */}
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 4 }}>
          <ShowChartIcon sx={{ mr: 1, fontSize: 28 }} />
          <Typography
            variant="h6"
            component="div"
            sx={{ fontWeight: 700, cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            Stock Tracker Pro
          </Typography>
        </Box>

        {/* Navigation Links */}
        <Box sx={{ display: 'flex', mr: 'auto' }}>
          {navigationItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                mr: 2,
                fontWeight: location.pathname === item.path ? 600 : 400,
                backgroundColor: location.pathname === item.path ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        {/* Search Bar */}
        <Box sx={{ width: 300 }}>
          <Autocomplete
            freeSolo
            options={searchResults}
            getOptionLabel={(option) => 
              typeof option === 'string' ? option : `${option.symbol} - ${option.name}`
            }
            loading={searchLoading}
            onInputChange={(event, newInputValue) => {
              setSearchQuery(newInputValue);
              handleSearch(newInputValue);
            }}
            onChange={(event, newValue) => {
              handleStockSelect(newValue);
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                placeholder="Search stocks..."
                size="small"
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    '& fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.3)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.5)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: 'white',
                    },
                  },
                  '& .MuiInputBase-input': {
                    color: 'white',
                    '&::placeholder': {
                      color: 'rgba(255, 255, 255, 0.7)',
                      opacity: 1,
                    },
                  },
                }}
                InputProps={{
                  ...params.InputProps,
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                    </InputAdornment>
                  ),
                }}
              />
            )}
            renderOption={(props, option) => (
              <Box component="li" {...props}>
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {option.symbol}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {option.name}
                  </Typography>
                </Box>
              </Box>
            )}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;