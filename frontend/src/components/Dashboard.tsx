import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Business as BusinessIcon,
  Assignment as AssignmentIcon,
  Warning as WarningIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { dashboardAPI, serviceAPI } from '../services/api';
import { DashboardStats, Service } from '../types';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [expiringServices, setExpiringServices] = useState<Service[]>([]);
  const [paymentDueServices, setPaymentDueServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [statsResponse, expiringResponse, paymentDueResponse] = await Promise.all([
          dashboardAPI.getStats(),
          serviceAPI.getExpiringSoon(),
          serviceAPI.getPaymentDueSoon(),
        ]);

        setStats(statsResponse.data as DashboardStats);
        setExpiringServices(expiringResponse.data as Service[]);
        setPaymentDueServices(paymentDueResponse.data as Service[]);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getStatusColor = (color: string) => {
    const colorMap: { [key: string]: string } = {
      red: '#f44336',
      orange: '#ff9800',
      green: '#4caf50',
      blue: '#2196f3',
    };
    return colorMap[color] || '#757575';
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <BusinessIcon color="primary" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Vendors
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_vendors || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {stats?.active_vendors || 0} active
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <AssignmentIcon color="primary" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Services
                  </Typography>
                  <Typography variant="h4">
                    {stats?.total_services || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {stats?.active_services || 0} active
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <WarningIcon color="warning" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Expiring Soon
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {stats?.expiring_soon || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Next 15 days
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <MoneyIcon color="success" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Value
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {formatCurrency(stats?.total_contract_value || 0)}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Active contracts
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Services Tables */}
      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 6 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom color="warning.main">
              Services Expiring Soon
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Service</TableCell>
                    <TableCell>Vendor</TableCell>
                    <TableCell>Expiry Date</TableCell>
                    <TableCell>Days Left</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {expiringServices.slice(0, 5).map((service) => (
                    <TableRow key={service.id}>
                      <TableCell>{service.service_name}</TableCell>
                      <TableCell>Vendor {service.vendor}</TableCell>
                      <TableCell>{new Date(service.expiry_date).toLocaleDateString()}</TableCell>
                      <TableCell>
                        <Chip
                          label={service.days_until_expiry}
                          color={service.days_until_expiry <= 7 ? 'error' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={service.status}
                          color={service.status === 'active' ? 'success' : service.status === 'expired' ? 'error' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom color="error.main">
              Payment Due Soon
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Service</TableCell>
                    <TableCell>Vendor</TableCell>
                    <TableCell>Due Date</TableCell>
                    <TableCell>Days Left</TableCell>
                    <TableCell>Amount</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {paymentDueServices.slice(0, 5).map((service) => (
                    <TableRow key={service.id}>
                      <TableCell>{service.service_name}</TableCell>
                      <TableCell>Vendor {service.vendor}</TableCell>
                      <TableCell>{new Date(service.payment_due_date).toLocaleDateString()}</TableCell>
                      <TableCell>
                        <Chip
                          label={service.days_until_payment_due}
                          color={service.days_until_payment_due <= 7 ? 'error' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{formatCurrency(service.amount)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
