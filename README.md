# Vendor Management System

A comprehensive vendor management system built with Django REST Framework backend and React frontend, featuring JWT authentication, automated reminders, and PostgreSQL database.

## Features

### Backend Features
- **Vendor Management**: CRUD operations for vendors with contact information
- **Service/Contract Management**: Manage multiple services per vendor with expiry and payment tracking
- **JWT Authentication**: Secure API access with token-based authentication
- **Automated Reminders**: Daily checks for expiring services and payment due dates
- **Email Notifications**: Automated email alerts for upcoming expirations and payments
- **RESTful API**: Complete API with pagination, filtering, and search capabilities
- **Admin Interface**: Django admin for system administration

### Frontend Features
- **Modern UI**: Material-UI based responsive interface
- **Dashboard**: Overview of vendors, services, and key metrics
- **Vendor Management**: Add, edit, delete, and view vendors
- **Service Management**: Comprehensive service/contract management
- **Real-time Status**: Color-coded status indicators for services
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

### Backend
- **Django 5.0.2**: Web framework
- **Django REST Framework**: API framework
- **PostgreSQL**: Database
- **Celery**: Task queue for background jobs
- **Redis**: Message broker for Celery
- **JWT**: Authentication
- **Email**: SMTP email notifications

### Frontend
- **React 18**: Frontend framework
- **TypeScript**: Type safety
- **Material-UI**: UI component library
- **Axios**: HTTP client
- **React Router**: Client-side routing
- **Date Pickers**: Date selection components

## Project Structure

```
vendor_management/
├── vendor_management_backend/     # Django backend
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL configuration
│   └── celery.py                 # Celery configuration
├── vendors/                      # Vendors app
│   ├── models.py                 # Vendor and Service models
│   ├── serializers.py            # API serializers
│   ├── views.py                  # API views
│   ├── urls.py                   # App URL configuration
│   └── admin.py                  # Admin configuration
├── notifications/                # Notifications app
│   ├── tasks.py                  # Celery tasks for reminders
│   └── signals.py                # Django signals
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── contexts/             # React contexts
│   │   ├── services/             # API services
│   │   └── types/                # TypeScript types
│   └── package.json
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

### Backend Setup

1. **Clone and navigate to the project directory:**
   ```bash
   cd ~/Documents/my_project/vendor_management
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE vendor_management;
   CREATE USER postgres WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE vendor_management TO postgres;
   ```

5. **Create environment file:**
   ```bash
   # Create .env file in the project root
   DB_NAME=vendor_management
   DB_USER=postgres
   DB_PASSWORD=password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@vendor-management.com
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

6. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start Redis server:**
   ```bash
   redis-server
   ```

9. **Start Celery worker (in a new terminal):**
   ```bash
   cd ~/Documents/my_project/vendor_management
   source venv/bin/activate
   celery -A vendor_management_backend worker --loglevel=info
   ```

10. **Start Celery beat for scheduled tasks (in another terminal):**
    ```bash
    cd ~/Documents/my_project/vendor_management
    source venv/bin/activate
    celery -A vendor_management_backend beat --loglevel=info
    ```

11. **Start Django development server:**
    ```bash
    python manage.py runserver
    ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ~/Documents/my_project/vendor_management/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   # Create .env.local file in frontend directory
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. **Start development server:**
   ```bash
   npm start
   ```

## API Documentation

### Authentication Endpoints

#### Login
- **POST** `/api/auth/login/`
- **Body:** `{"username": "string", "password": "string"}`
- **Response:** `{"access": "string", "refresh": "string"}`

#### Refresh Token
- **POST** `/api/auth/refresh/`
- **Body:** `{"refresh": "string"}`
- **Response:** `{"access": "string"}`

### Vendor Endpoints

#### List Vendors
- **GET** `/api/vendors/`
- **Query Parameters:** `page`, `status`, `search`, `ordering`
- **Response:** Paginated list of vendors

#### Get Vendor
- **GET** `/api/vendors/{id}/`
- **Response:** Single vendor with services

#### Create Vendor
- **POST** `/api/vendors/`
- **Body:** `{"name": "string", "contact_person": "string", "email": "string", "phone": "string", "status": "active|inactive"}`
- **Response:** Created vendor

#### Update Vendor
- **PATCH** `/api/vendors/{id}/`
- **Body:** Partial vendor data
- **Response:** Updated vendor

#### Delete Vendor
- **DELETE** `/api/vendors/{id}/`
- **Response:** 204 No Content

#### Get Vendors with Active Services
- **GET** `/api/vendors/with-active-services/`
- **Response:** List of vendors with active services

### Service Endpoints

#### List Services
- **GET** `/api/services/`
- **Query Parameters:** `page`, `vendor`, `status`, `search`, `ordering`
- **Response:** Paginated list of services

#### Get Service
- **GET** `/api/services/{id}/`
- **Response:** Single service

#### Create Service
- **POST** `/api/services/`
- **Body:** `{"vendor": "int", "service_name": "string", "start_date": "YYYY-MM-DD", "expiry_date": "YYYY-MM-DD", "payment_due_date": "YYYY-MM-DD", "amount": "decimal", "status": "active|expired|payment_pending|completed"}`
- **Response:** Created service

#### Update Service
- **PATCH** `/api/services/{id}/`
- **Body:** Partial service data
- **Response:** Updated service

#### Delete Service
- **DELETE** `/api/services/{id}/`
- **Response:** 204 No Content

#### Update Service Status
- **PATCH** `/api/services/{id}/status/`
- **Body:** `{"status": "active|expired|payment_pending|completed"}`
- **Response:** Updated service

#### Get Services Expiring Soon
- **GET** `/api/services/expiring-soon/`
- **Response:** List of services expiring in next 15 days

#### Get Services Payment Due Soon
- **GET** `/api/services/payment-due-soon/`
- **Response:** List of services with payment due in next 15 days

### Dashboard Endpoints

#### Get Dashboard Statistics
- **GET** `/api/dashboard/stats/`
- **Response:** Dashboard statistics object

#### Get Service Reminders
- **GET** `/api/reminders/`
- **Response:** List of service reminders

## Database Schema

### Vendor Model
- `id`: Primary key
- `name`: Vendor name (unique)
- `contact_person`: Contact person name
- `email`: Email address (unique)
- `phone`: Phone number
- `status`: Active/Inactive
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `created_by`: User who created the vendor

### Service Model
- `id`: Primary key
- `vendor`: Foreign key to Vendor
- `service_name`: Name of the service
- `start_date`: Service start date
- `expiry_date`: Service expiry date
- `payment_due_date`: Payment due date
- `amount`: Service amount
- `status`: Active/Expired/Payment Pending/Completed
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `created_by`: User who created the service

### ServiceReminder Model
- `id`: Primary key
- `service`: Foreign key to Service
- `reminder_type`: Expiry/Payment reminder
- `reminder_date`: Date of reminder
- `is_sent`: Whether reminder was sent
- `sent_at`: When reminder was sent
- `created_at`: Creation timestamp

## Design Choices

### Backend Design
1. **Django REST Framework**: Chosen for its robust API capabilities and built-in features
2. **PostgreSQL**: Reliable, ACID-compliant database for production use
3. **JWT Authentication**: Stateless authentication suitable for API-based applications
4. **Celery**: Asynchronous task processing for email notifications
5. **Redis**: Fast in-memory data store for Celery message broker
6. **Django Signals**: Automatic reminder creation when services are created/updated

### Frontend Design
1. **React with TypeScript**: Type safety and modern development experience
2. **Material-UI**: Consistent, accessible UI components
3. **Context API**: State management for authentication
4. **Axios Interceptors**: Automatic token refresh and error handling
5. **Responsive Design**: Mobile-first approach for better user experience

### Security Considerations
1. **JWT Tokens**: Secure, stateless authentication
2. **CORS Configuration**: Proper cross-origin resource sharing setup
3. **Input Validation**: Both client and server-side validation
4. **SQL Injection Protection**: Django ORM prevents SQL injection
5. **XSS Protection**: Django's built-in XSS protection

## Usage

1. **Access the application**: Navigate to `http://localhost:3000`
2. **Login**: Use the superuser credentials created during setup
3. **Manage Vendors**: Add, edit, and manage vendor information
4. **Manage Services**: Create and track service contracts
5. **Monitor Dashboard**: View key metrics and upcoming deadlines
6. **Admin Interface**: Access Django admin at `http://localhost:8000/admin/`

## API Testing

The API includes Swagger documentation available at:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Ensure PostgreSQL is running and credentials are correct
2. **Redis Connection Error**: Make sure Redis server is running
3. **Celery Tasks Not Running**: Check if Celery worker and beat are running
4. **CORS Errors**: Verify CORS settings in Django settings
5. **Token Expired**: Check JWT token expiration settings

### Logs
- Django logs: Check console output
- Celery logs: Check worker and beat console output
- Frontend logs: Check browser console

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.
