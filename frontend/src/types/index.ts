export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Vendor {
  id: number;
  name: string;
  contact_person: string;
  email: string;
  phone: string;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
  created_by: User;
  services?: Service[];
}

export interface Service {
  id: number;
  vendor: number;
  service_name: string;
  start_date: string;
  expiry_date: string;
  payment_due_date: string;
  amount: number;
  status: 'active' | 'expired' | 'payment_pending' | 'completed';
  created_at: string;
  updated_at: string;
  created_by: User;
  days_until_expiry: number;
  days_until_payment_due: number;
  is_expiring_soon: boolean;
  is_payment_due_soon: boolean;
}

export interface ServiceReminder {
  id: number;
  service: Service;
  reminder_type: 'expiry' | 'payment';
  reminder_date: string;
  is_sent: boolean;
  sent_at?: string;
  created_at: string;
}

export interface DashboardStats {
  total_vendors: number;
  active_vendors: number;
  total_services: number;
  active_services: number;
  expiring_soon: number;
  payment_due_soon: number;
  overdue_services: number;
  total_contract_value: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface CreateVendorData {
  name: string;
  contact_person: string;
  email: string;
  phone: string;
  status: 'active' | 'inactive';
}

export interface CreateServiceData {
  vendor: number;
  service_name: string;
  start_date: string;
  expiry_date: string;
  payment_due_date: string;
  amount: number;
  status: 'active' | 'expired' | 'payment_pending' | 'completed';
}

export interface UpdateServiceStatusData {
  status: 'active' | 'expired' | 'payment_pending' | 'completed';
}
