from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Vendor, Service
from .serializers import (
    VendorSerializer, ServiceSerializer, ServiceCreateSerializer,
    VendorListSerializer, ServiceStatusUpdateSerializer
)


class VendorListCreateView(generics.ListCreateAPIView):
    """Handle listing and creating vendors"""
    
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        # Use different serializer for list vs create
        if self.request.method == 'GET':
            return VendorListSerializer
        return VendorSerializer
    
    def perform_create(self, serializer):
        # Set the creator to current user
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
def services_expiring_soon(request):
    """Get services that expire within 15 days"""
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
    """Get services with payment due within 15 days"""
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
    """Update service status (active, expired, etc.)"""
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
def dashboard_stats(request):
    """Get basic dashboard statistics for the frontend"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    # Basic counts
    total_vendors = Vendor.objects.count()
    active_vendors = Vendor.objects.filter(status='active').count()
    total_services = Service.objects.count()
    active_services = Service.objects.filter(status='active').count()
    
    # Expiring and payment due counts
    expiring_soon = Service.objects.filter(
        expiry_date__range=[today, fifteen_days_later],
        status='active'
    ).count()
    
    payment_due_soon = Service.objects.filter(
        payment_due_date__range=[today, fifteen_days_later],
        status__in=['active', 'payment_pending']
    ).count()
    
    # Overdue services (past due date)
    overdue_services = Service.objects.filter(
        payment_due_date__lt=today,
        status__in=['active', 'payment_pending']
    ).count()
    
    # Total contract value
    total_contract_value = Service.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    stats = {
        'total_vendors': total_vendors,
        'active_vendors': active_vendors,
        'total_services': total_services,
        'active_services': active_services,
        'expiring_soon': expiring_soon,
        'payment_due_soon': payment_due_soon,
        'overdue_services': overdue_services,
        'total_contract_value': float(total_contract_value),
    }
    
    return Response(stats)

