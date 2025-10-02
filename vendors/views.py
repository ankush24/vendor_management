from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Vendor, Service, ServiceReminder
from .serializers import (
    VendorSerializer, ServiceSerializer, ServiceCreateSerializer,
    VendorListSerializer, ServiceStatusUpdateSerializer, ServiceReminderSerializer
)


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VendorListSerializer
        return VendorSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)


class ServiceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendor', 'status']
    search_fields = ['service_name', 'vendor__name']
    ordering_fields = ['service_name', 'start_date', 'expiry_date', 'payment_due_date', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Service.objects.select_related('vendor', 'created_by')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ServiceSerializer
        return ServiceCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.select_related('vendor', 'created_by')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendors_with_active_services(request):
    """List all vendors with their active services"""
    vendors = Vendor.objects.filter(
        status='active',
        services__status='active'
    ).distinct().prefetch_related('services')
    
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def services_expiring_soon(request):
    """Get all services expiring in the next 15 days"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    services = Service.objects.filter(
        expiry_date__range=[today, fifteen_days_later],
        status='active'
    ).select_related('vendor', 'created_by')
    
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def services_payment_due_soon(request):
    """Get all services with payment due in the next 15 days"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    services = Service.objects.filter(
        payment_due_date__range=[today, fifteen_days_later],
        status__in=['active', 'payment_pending']
    ).select_related('vendor', 'created_by')
    
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_service_status(request, pk):
    """Update contract/service status"""
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response(
            {'error': 'Service not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ServiceStatusUpdateSerializer(service, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def service_reminders(request):
    """Get all service reminders"""
    reminders = ServiceReminder.objects.select_related('service__vendor').order_by('-created_at')
    serializer = ServiceReminderSerializer(reminders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    stats = {
        'total_vendors': Vendor.objects.count(),
        'active_vendors': Vendor.objects.filter(status='active').count(),
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(status='active').count(),
        'expiring_soon': Service.objects.filter(
            expiry_date__range=[today, fifteen_days_later],
            status='active'
        ).count(),
        'payment_due_soon': Service.objects.filter(
            payment_due_date__range=[today, fifteen_days_later],
            status__in=['active', 'payment_pending']
        ).count(),
        'overdue_services': Service.objects.filter(
            Q(expiry_date__lt=today) | Q(payment_due_date__lt=today),
            status='active'
        ).count(),
        'total_contract_value': sum(
            service.amount for service in Service.objects.filter(status='active')
        )
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_services(request, vendor_id):
    """Get all services for a specific vendor"""
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(
            {'error': 'Vendor not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    services = vendor.services.all().select_related('created_by')
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)