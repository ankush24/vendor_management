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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { vendorAPI } from '../services/api';
import { Vendor, CreateVendorData } from '../types';

const Vendors: React.FC = () => {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [editingVendor, setEditingVendor] = useState<Vendor | null>(null);
  const [formData, setFormData] = useState<CreateVendorData>({
    name: '',
    contact_person: '',
    email: '',
    phone: '',
    status: 'active',
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchVendors();
  }, [page]);

  const fetchVendors = async () => {
    try {
      setLoading(true);
      const response = await vendorAPI.getVendors({ page });
      const data = response.data as any;
      setVendors(data.results);
      setTotalPages(Math.ceil(data.count / 20));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load vendors');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (vendor?: Vendor) => {
    if (vendor) {
      setEditingVendor(vendor);
      setFormData({
        name: vendor.name,
        contact_person: vendor.contact_person,
        email: vendor.email,
        phone: vendor.phone,
        status: vendor.status,
      });
    } else {
      setEditingVendor(null);
      setFormData({
        name: '',
        contact_person: '',
        email: '',
        phone: '',
        status: 'active',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingVendor(null);
    setFormData({
      name: '',
      contact_person: '',
      email: '',
      phone: '',
      status: 'active',
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingVendor) {
        await vendorAPI.updateVendor(editingVendor.id, formData);
      } else {
        await vendorAPI.createVendor(formData);
      }
      handleClose();
      fetchVendors();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save vendor');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this vendor?')) {
      try {
        await vendorAPI.deleteVendor(id);
        fetchVendors();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete vendor');
      }
    }
  };

  const getStatusColor = (status: string) => {
    return status === 'active' ? 'success' : 'default';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Vendors</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Add Vendor
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
              <TableCell>Name</TableCell>
              <TableCell>Contact Person</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {vendors.map((vendor) => (
              <TableRow key={vendor.id}>
                <TableCell>{vendor.name}</TableCell>
                <TableCell>{vendor.contact_person}</TableCell>
                <TableCell>{vendor.email}</TableCell>
                <TableCell>{vendor.phone}</TableCell>
                <TableCell>
                  <Chip
                    label={vendor.status}
                    color={getStatusColor(vendor.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleOpen(vendor)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(vendor.id)}
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

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingVendor ? 'Edit Vendor' : 'Add New Vendor'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Vendor Name"
              fullWidth
              variant="outlined"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
            <TextField
              margin="dense"
              label="Contact Person"
              fullWidth
              variant="outlined"
              value={formData.contact_person}
              onChange={(e) => setFormData({ ...formData, contact_person: e.target.value })}
              required
            />
            <TextField
              margin="dense"
              label="Email"
              type="email"
              fullWidth
              variant="outlined"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
            <TextField
              margin="dense"
              label="Phone"
              fullWidth
              variant="outlined"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              required
            />
            <FormControl fullWidth margin="dense">
              <InputLabel>Status</InputLabel>
              <Select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value as 'active' | 'inactive' })}
                label="Status"
              >
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="inactive">Inactive</MenuItem>
              </Select>
            </FormControl>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button type="submit" variant="contained">
              {editingVendor ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Vendors;
