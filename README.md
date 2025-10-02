# Vendor Management System

A simple system I built to manage vendors and their contracts. It helps keep track of when contracts expire and when payments are due.

## What it does

This system lets you:
- Add and manage vendors (companies you work with)
- Create services/contracts for each vendor
- See which contracts are expiring soon (within 15 days)
- Get email reminders when contracts are about to expire
- Update contract statuses (active, expired, payment pending, completed)

## Tech stack

**Backend:**
- Django with REST API
- PostgreSQL database
- Celery for background email tasks
- Redis for task queue
- JWT for authentication

**Frontend:**
- React with TypeScript
- Material-UI for the interface
- Axios for API calls

## Setup

### Prerequisites
You'll need:
- Python 3.11+
- Node.js 16+
- PostgreSQL
- Redis

### Backend setup

1. Clone the repo and cd into it
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   ```bash
   # Create database
   createdb vendor_management
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE vendor_management;
   CREATE USER vendor_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE vendor_management TO vendor_user;
   ```

5. Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=vendor_management
   DB_USER=vendor_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@yourcompany.com
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Start the backend:
   ```bash
   python manage.py runserver
   ```

9. In another terminal, start Celery worker:
   ```bash
   celery -A vendor_management_backend worker --loglevel=info
   ```

10. Start Celery beat (for scheduled tasks):
    ```bash
    celery -A vendor_management_backend beat --loglevel=info
    ```

### Frontend setup

1. Go to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. Start the frontend:
   ```bash
   npm start
   ```

The app should be running at http://localhost:3000

## API endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token

### Vendors
- `GET /api/vendors/` - List vendors
- `POST /api/vendors/` - Create vendor
- `GET /api/vendors/{id}/` - Get vendor details
- `PATCH /api/vendors/{id}/` - Update vendor
- `DELETE /api/vendors/{id}/` - Delete vendor

### Services
- `GET /api/services/` - List services
- `POST /api/services/` - Create service
- `GET /api/services/{id}/` - Get service details
- `PATCH /api/services/{id}/` - Update service
- `DELETE /api/services/{id}/` - Delete service
- `PATCH /api/services/{id}/status/` - Update service status

### Required APIs (as per requirements)
- `GET /api/vendors/` - List all vendors with their active services
- `GET /api/services/expiring-soon/` - Get services expiring in next 15 days
- `GET /api/services/payment-due-soon/` - Get services with payment due in next 15 days

## Sample API calls

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Get Vendors
```bash
curl -X GET http://localhost:8000/api/vendors/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Vendor
```bash
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ABC Company",
    "contact_person": "John Doe",
    "email": "john@abc.com",
    "phone": "+1234567890",
    "status": "active"
  }'
```

### Create Service
```bash
curl -X POST http://localhost:8000/api/services/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "service_name": "Web Development",
    "start_date": "2024-01-01",
    "expiry_date": "2024-12-31",
    "payment_due_date": "2024-06-30",
    "amount": 50000.00,
    "status": "active"
  }'
```

## Database models

### Vendor
- `name` - Company name
- `contact_person` - Contact person name
- `email` - Contact email
- `phone` - Phone number
- `status` - Active/Inactive
- `created_at` - When it was created
- `updated_at` - Last update time
- `created_by` - Who created it

### Service
- `vendor` - Which vendor this belongs to
- `service_name` - Name of the service/contract
- `start_date` - When the service starts
- `expiry_date` - When the service expires
- `payment_due_date` - When payment is due
- `amount` - Contract amount
- `status` - Active/Expired/Payment Pending/Completed
- `created_at` - When it was created
- `updated_at` - Last update time
- `created_by` - Who created it

## How reminders work

The system automatically:
1. Checks daily for services expiring in the next 15 days
2. Sends email alerts to vendor contacts and service creators
3. Updates service status based on dates (expires automatically when past expiry date)

## Why I built it this way

- **Django**: I'm familiar with it and it's great for APIs
- **PostgreSQL**: Reliable database that handles relationships well
- **Celery**: Needed for background email tasks
- **React**: Good for building interactive UIs
- **JWT**: Simple authentication that works well with APIs

## Notes

- All API calls need authentication except login
- The system automatically updates service status based on dates
- Email reminders are sent in the background
- Frontend uses JWT tokens for API calls

## Troubleshooting

- Make sure PostgreSQL and Redis are running
- Check that all environment variables are set
- Make sure the database exists and migrations are applied
- Check Celery logs if emails aren't being sent