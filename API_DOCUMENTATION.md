# Vendor Management System - API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All API endpoints require JWT authentication except for login and refresh token endpoints.

### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Authentication Endpoints

### Login
**POST** `/auth/login/`

Authenticate user and receive access and refresh tokens.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Status Codes:**
- `200 OK`: Login successful
- `401 Unauthorized`: Invalid credentials

### Refresh Token
**POST** `/auth/refresh/`

Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh": "string"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Vendor Endpoints

### List Vendors
**GET** `/vendors/`

Get paginated list of vendors with optional filtering and search.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `status` (string): Filter by status (`active`, `inactive`)
- `search` (string): Search in name, contact_person, email
- `ordering` (string): Order by field (`name`, `created_at`, `updated_at`)

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/vendors/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "ABC Corporation",
      "contact_person": "John Doe",
      "email": "john@abc.com",
      "phone": "+1234567890",
      "status": "active",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "",
        "last_name": ""
      },
      "active_services_count": 3,
      "total_contract_value": 15000.00
    }
  ]
}
```

### Get Vendor
**GET** `/vendors/{id}/`

Get detailed information about a specific vendor including all services.

**Response:**
```json
{
  "id": 1,
  "name": "ABC Corporation",
  "contact_person": "John Doe",
  "email": "john@abc.com",
  "phone": "+1234567890",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "services": [
    {
      "id": 1,
      "vendor": 1,
      "service_name": "Web Development",
      "start_date": "2024-01-01",
      "expiry_date": "2024-12-31",
      "payment_due_date": "2024-01-15",
      "amount": 5000.00,
      "status": "active",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "",
        "last_name": ""
      },
      "days_until_expiry": 300,
      "days_until_payment_due": 10,
      "is_expiring_soon": false,
      "is_payment_due_soon": true,
      "is_overdue": false,
      "status_color": "blue"
    }
  ],
  "active_services_count": 3,
  "total_contract_value": 15000.00
}
```

### Create Vendor
**POST** `/vendors/`

Create a new vendor.

**Request Body:**
```json
{
  "name": "ABC Corporation",
  "contact_person": "John Doe",
  "email": "john@abc.com",
  "phone": "+1234567890",
  "status": "active"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "ABC Corporation",
  "contact_person": "John Doe",
  "email": "john@abc.com",
  "phone": "+1234567890",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "active_services_count": 0,
  "total_contract_value": 0.00
}
```

### Update Vendor
**PATCH** `/vendors/{id}/`

Update an existing vendor.

**Request Body:**
```json
{
  "name": "ABC Corporation Updated",
  "status": "inactive"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "ABC Corporation Updated",
  "contact_person": "John Doe",
  "email": "john@abc.com",
  "phone": "+1234567890",
  "status": "inactive",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "active_services_count": 0,
  "total_contract_value": 0.00
}
```

### Delete Vendor
**DELETE** `/vendors/{id}/`

Delete a vendor.

**Response:**
```
204 No Content
```

### Get Vendors with Active Services
**GET** `/vendors/with-active-services/`

Get all vendors that have active services.

**Response:**
```json
[
  {
    "id": 1,
    "name": "ABC Corporation",
    "contact_person": "John Doe",
    "email": "john@abc.com",
    "phone": "+1234567890",
    "status": "active",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "created_by": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "first_name": "",
      "last_name": ""
    },
    "services": [
      {
        "id": 1,
        "vendor": 1,
        "service_name": "Web Development",
        "start_date": "2024-01-01",
        "expiry_date": "2024-12-31",
        "payment_due_date": "2024-01-15",
        "amount": 5000.00,
        "status": "active",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
        "created_by": {
          "id": 1,
          "username": "admin",
          "email": "admin@example.com",
          "first_name": "",
          "last_name": ""
        },
        "days_until_expiry": 300,
        "days_until_payment_due": 10,
        "is_expiring_soon": false,
        "is_payment_due_soon": true,
        "is_overdue": false,
        "status_color": "blue"
      }
    ],
    "active_services_count": 1,
    "total_contract_value": 5000.00
  }
]
```

## Service Endpoints

### List Services
**GET** `/services/`

Get paginated list of services with optional filtering and search.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `vendor` (int): Filter by vendor ID
- `status` (string): Filter by status (`active`, `expired`, `payment_pending`, `completed`)
- `search` (string): Search in service_name, vendor name
- `ordering` (string): Order by field (`service_name`, `start_date`, `expiry_date`, `payment_due_date`, `amount`)

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/services/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "vendor": 1,
      "service_name": "Web Development",
      "start_date": "2024-01-01",
      "expiry_date": "2024-12-31",
      "payment_due_date": "2024-01-15",
      "amount": 5000.00,
      "status": "active",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "",
        "last_name": ""
      },
      "days_until_expiry": 300,
      "days_until_payment_due": 10,
      "is_expiring_soon": false,
      "is_payment_due_soon": true,
      "is_overdue": false,
      "status_color": "blue"
    }
  ]
}
```

### Get Service
**GET** `/services/{id}/`

Get detailed information about a specific service.

**Response:**
```json
{
  "id": 1,
  "vendor": 1,
  "service_name": "Web Development",
  "start_date": "2024-01-01",
  "expiry_date": "2024-12-31",
  "payment_due_date": "2024-01-15",
  "amount": 5000.00,
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "days_until_expiry": 300,
  "days_until_payment_due": 10,
  "is_expiring_soon": false,
  "is_payment_due_soon": true,
  "is_overdue": false,
  "status_color": "blue"
}
```

### Create Service
**POST** `/services/`

Create a new service.

**Request Body:**
```json
{
  "vendor": 1,
  "service_name": "Web Development",
  "start_date": "2024-01-01",
  "expiry_date": "2024-12-31",
  "payment_due_date": "2024-01-15",
  "amount": 5000.00,
  "status": "active"
}
```

**Response:**
```json
{
  "id": 1,
  "vendor": 1,
  "service_name": "Web Development",
  "start_date": "2024-01-01",
  "expiry_date": "2024-12-31",
  "payment_due_date": "2024-01-15",
  "amount": 5000.00,
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "days_until_expiry": 300,
  "days_until_payment_due": 10,
  "is_expiring_soon": false,
  "is_payment_due_soon": true,
  "is_overdue": false,
  "status_color": "blue"
}
```

### Update Service
**PATCH** `/services/{id}/`

Update an existing service.

**Request Body:**
```json
{
  "service_name": "Web Development Updated",
  "amount": 6000.00
}
```

**Response:**
```json
{
  "id": 1,
  "vendor": 1,
  "service_name": "Web Development Updated",
  "start_date": "2024-01-01",
  "expiry_date": "2024-12-31",
  "payment_due_date": "2024-01-15",
  "amount": 6000.00,
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "days_until_expiry": 300,
  "days_until_payment_due": 10,
  "is_expiring_soon": false,
  "is_payment_due_soon": true,
  "is_overdue": false,
  "status_color": "blue"
}
```

### Delete Service
**DELETE** `/services/{id}/`

Delete a service.

**Response:**
```
204 No Content
```

### Update Service Status
**PATCH** `/services/{id}/status/`

Update the status of a service.

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:**
```json
{
  "id": 1,
  "vendor": 1,
  "service_name": "Web Development",
  "start_date": "2024-01-01",
  "expiry_date": "2024-12-31",
  "payment_due_date": "2024-01-15",
  "amount": 5000.00,
  "status": "completed",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  },
  "days_until_expiry": 300,
  "days_until_payment_due": 10,
  "is_expiring_soon": false,
  "is_payment_due_soon": true,
  "is_overdue": false,
  "status_color": "green"
}
```

### Get Services Expiring Soon
**GET** `/services/expiring-soon/`

Get all services expiring in the next 15 days.

**Response:**
```json
[
  {
    "id": 1,
    "vendor": 1,
    "service_name": "Web Development",
    "start_date": "2024-01-01",
    "expiry_date": "2024-01-20",
    "payment_due_date": "2024-01-15",
    "amount": 5000.00,
    "status": "active",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "created_by": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "first_name": "",
      "last_name": ""
    },
    "days_until_expiry": 5,
    "days_until_payment_due": 0,
    "is_expiring_soon": true,
    "is_payment_due_soon": true,
    "is_overdue": true,
    "status_color": "red"
  }
]
```

### Get Services Payment Due Soon
**GET** `/services/payment-due-soon/`

Get all services with payment due in the next 15 days.

**Response:**
```json
[
  {
    "id": 1,
    "vendor": 1,
    "service_name": "Web Development",
    "start_date": "2024-01-01",
    "expiry_date": "2024-12-31",
    "payment_due_date": "2024-01-20",
    "amount": 5000.00,
    "status": "active",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "created_by": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "first_name": "",
      "last_name": ""
    },
    "days_until_expiry": 300,
    "days_until_payment_due": 5,
    "is_expiring_soon": false,
    "is_payment_due_soon": true,
    "is_overdue": false,
    "status_color": "orange"
  }
]
```

## Dashboard Endpoints

### Get Dashboard Statistics
**GET** `/dashboard/stats/`

Get comprehensive dashboard statistics.

**Response:**
```json
{
  "total_vendors": 25,
  "active_vendors": 20,
  "total_services": 150,
  "active_services": 120,
  "expiring_soon": 5,
  "payment_due_soon": 8,
  "overdue_services": 3,
  "total_contract_value": 250000.00
}
```

### Get Service Reminders
**GET** `/reminders/`

Get all service reminders.

**Response:**
```json
[
  {
    "id": 1,
    "service": {
      "id": 1,
      "vendor": 1,
      "service_name": "Web Development",
      "start_date": "2024-01-01",
      "expiry_date": "2024-01-20",
      "payment_due_date": "2024-01-15",
      "amount": 5000.00,
      "status": "active",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "",
        "last_name": ""
      },
      "days_until_expiry": 5,
      "days_until_payment_due": 0,
      "is_expiring_soon": true,
      "is_payment_due_soon": true,
      "is_overdue": true,
      "status_color": "red"
    },
    "reminder_type": "expiry",
    "reminder_date": "2024-01-15",
    "is_sent": true,
    "sent_at": "2024-01-15T09:00:00Z",
    "created_at": "2024-01-15T08:00:00Z"
  }
]
```

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content returned
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (1-based)
- `page_size`: Number of items per page (default: 20)

Response includes:
- `count`: Total number of items
- `next`: URL for next page (null if last page)
- `previous`: URL for previous page (null if first page)
- `results`: Array of items for current page
