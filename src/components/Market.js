import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import Dashboard from './Dashboard';

const Market = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Market Overview
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Explore trending stocks and market data
        </Typography>
      </Box>
      
      {/* Reuse Dashboard trending stocks component */}
      <Dashboard />
    </Container>
  );
};

export default Market;