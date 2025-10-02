from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Vendors
    path('vendors/', views.VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/<int:vendor_id>/services/', views.vendor_services, name='vendor-services'),
    path('vendors/with-active-services/', views.vendors_with_active_services, name='vendors-active-services'),
    
    # Services
    path('services/', views.ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:pk>/status/', views.update_service_status, name='service-status-update'),
    path('services/expiring-soon/', views.services_expiring_soon, name='services-expiring-soon'),
    path('services/payment-due-soon/', views.services_payment_due_soon, name='services-payment-due-soon'),
    
    # Dashboard and Analytics
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('reminders/', views.service_reminders, name='service-reminders'),
]
