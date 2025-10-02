import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Pagination,
  Grid,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Update as UpdateIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import { serviceAPI, vendorAPI } from '../services/api';
import { Service, CreateServiceData, Vendor, UpdateServiceStatusData } from '../types';

const Services: React.FC = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [statusOpen, setStatusOpen] = useState(false);
  const [editingService, setEditingService] = useState<Service | null>(null);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [formData, setFormData] = useState<CreateServiceData>({
    vendor: 0,
    service_name: '',
    start_date: '',
    expiry_date: '',
    payment_due_date: '',
    amount: 0,
    status: 'active',
  });
  const [statusData, setStatusData] = useState<UpdateServiceStatusData>({
    status: 'active',
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchServices();
    fetchVendors();
  }, [page]);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await serviceAPI.getServices({ page });
      const data = response.data as any;
      setServices(data.results);
      setTotalPages(Math.ceil(data.count / 20));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load services');
    } finally {
      setLoading(false);
    }
  };

  const fetchVendors = async () => {
    try {
      const response = await vendorAPI.getVendors();
      const data = response.data as any;
      setVendors(data.results);
    } catch (err: any) {
      console.error('Failed to load vendors:', err);
    }
  };

  const handleOpen = (service?: Service) => {
    if (service) {
      setEditingService(service);
      setFormData({
        vendor: service.vendor,
        service_name: service.service_name,
        start_date: service.start_date,
        expiry_date: service.expiry_date,
        payment_due_date: service.payment_due_date,
        amount: service.amount,
        status: service.status,
      });
    } else {
      setEditingService(null);
      setFormData({
        vendor: 0,
        service_name: '',
        start_date: '',
        expiry_date: '',
        payment_due_date: '',
        amount: 0,
        status: 'active',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingService(null);
    setFormData({
      vendor: 0,
      service_name: '',
      start_date: '',
      expiry_date: '',
      payment_due_date: '',
      amount: 0,
      status: 'active',
    });
  };

  const handleStatusOpen = (service: Service) => {
    setSelectedService(service);
    setStatusData({ status: service.status });
    setStatusOpen(true);
  };

  const handleStatusClose = () => {
    setStatusOpen(false);
    setSelectedService(null);
    setStatusData({ status: 'active' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingService) {
        await serviceAPI.updateService(editingService.id, formData);
      } else {
        await serviceAPI.createService(formData);
      }
      handleClose();
      fetchServices();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save service');
    }
  };

  const handleStatusSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedService) {
      try {
        await serviceAPI.updateServiceStatus(selectedService.id, statusData.status);
        handleStatusClose();
        fetchServices();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to update service status');
      }
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this service?')) {
      try {
        await serviceAPI.deleteService(id);
        fetchServices();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete service');
      }
    }
  };

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

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4">Services</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpen()}
          >
            Add Service
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Service Name</TableCell>
                <TableCell>Vendor</TableCell>
                <TableCell>Start Date</TableCell>
                <TableCell>Expiry Date</TableCell>
                <TableCell>Payment Due</TableCell>
                <TableCell>Amount</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Days Left</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {services.map((service) => (
                <TableRow key={service.id}>
                  <TableCell>{service.service_name}</TableCell>
                  <TableCell>
                    {vendors.find(v => v.id === service.vendor)?.name || `Vendor ${service.vendor}`}
                  </TableCell>
                  <TableCell>{new Date(service.start_date).toLocaleDateString()}</TableCell>
                  <TableCell>{new Date(service.expiry_date).toLocaleDateString()}</TableCell>
                  <TableCell>{new Date(service.payment_due_date).toLocaleDateString()}</TableCell>
                  <TableCell>{formatCurrency(service.amount)}</TableCell>
                  <TableCell>
                    <Chip
                      label={service.status}
                      color={service.status === 'active' ? 'success' : service.status === 'expired' ? 'error' : 'warning'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Chip
                        label={`Exp: ${service.days_until_expiry}`}
                        color={service.is_expiring_soon ? 'warning' : 'default'}
                        size="small"
                        sx={{ mr: 1 }}
                      />
                      <Chip
                        label={`Pay: ${service.days_until_payment_due}`}
                        color={service.is_payment_due_soon ? 'warning' : 'default'}
                        size="small"
                      />
                    </Box>
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleOpen(service)}
                      color="primary"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleStatusOpen(service)}
                      color="secondary"
                    >
                      <UpdateIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(service.id)}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {totalPages > 1 && (
          <Box display="flex" justifyContent="center" mt={3}>
            <Pagination
              count={totalPages}
              page={page}
              onChange={(_, value) => setPage(value)}
              color="primary"
            />
          </Box>
        )}

        {/* Add/Edit Service Dialog */}
        <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
          <DialogTitle>
            {editingService ? 'Edit Service' : 'Add New Service'}
          </DialogTitle>
          <form onSubmit={handleSubmit}>
            <DialogContent>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <FormControl fullWidth margin="dense">
                    <InputLabel>Vendor</InputLabel>
                    <Select
                      value={formData.vendor}
                      onChange={(e) => setFormData({ ...formData, vendor: Number(e.target.value) })}
                      label="Vendor"
                      required
                    >
                      {vendors.map((vendor) => (
                        <MenuItem key={vendor.id} value={vendor.id}>
                          {vendor.name}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    margin="dense"
                    label="Service Name"
                    fullWidth
                    variant="outlined"
                    value={formData.service_name}
                    onChange={(e) => setFormData({ ...formData, service_name: e.target.value })}
                    required
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <DatePicker
                    label="Start Date"
                    value={formData.start_date ? dayjs(formData.start_date) : null}
                    onChange={(date) => setFormData({ ...formData, start_date: date?.format('YYYY-MM-DD') || '' })}
                    slotProps={{ textField: { fullWidth: true, margin: 'dense' } }}
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <DatePicker
                    label="Expiry Date"
                    value={formData.expiry_date ? dayjs(formData.expiry_date) : null}
                    onChange={(date) => setFormData({ ...formData, expiry_date: date?.format('YYYY-MM-DD') || '' })}
                    slotProps={{ textField: { fullWidth: true, margin: 'dense' } }}
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <DatePicker
                    label="Payment Due Date"
                    value={formData.payment_due_date ? dayjs(formData.payment_due_date) : null}
                    onChange={(date) => setFormData({ ...formData, payment_due_date: date?.format('YYYY-MM-DD') || '' })}
                    slotProps={{ textField: { fullWidth: true, margin: 'dense' } }}
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    margin="dense"
                    label="Amount"
                    type="number"
                    fullWidth
                    variant="outlined"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: Number(e.target.value) })}
                    required
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <FormControl fullWidth margin="dense">
                    <InputLabel>Status</InputLabel>
                    <Select
                      value={formData.status}
                      onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
                      label="Status"
                    >
                      <MenuItem value="active">Active</MenuItem>
                      <MenuItem value="expired">Expired</MenuItem>
                      <MenuItem value="payment_pending">Payment Pending</MenuItem>
                      <MenuItem value="completed">Completed</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose}>Cancel</Button>
              <Button type="submit" variant="contained">
                {editingService ? 'Update' : 'Create'}
              </Button>
            </DialogActions>
          </form>
        </Dialog>

        {/* Update Status Dialog */}
        <Dialog open={statusOpen} onClose={handleStatusClose} maxWidth="sm" fullWidth>
          <DialogTitle>Update Service Status</DialogTitle>
          <form onSubmit={handleStatusSubmit}>
            <DialogContent>
              <Typography variant="body1" gutterBottom>
                Service: {selectedService?.service_name}
              </Typography>
              <FormControl fullWidth margin="dense">
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusData.status}
                  onChange={(e) => setStatusData({ status: e.target.value as any })}
                  label="Status"
                >
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="expired">Expired</MenuItem>
                  <MenuItem value="payment_pending">Payment Pending</MenuItem>
                  <MenuItem value="completed">Completed</MenuItem>
                </Select>
              </FormControl>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleStatusClose}>Cancel</Button>
              <Button type="submit" variant="contained">
                Update Status
              </Button>
            </DialogActions>
          </form>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default Services;
