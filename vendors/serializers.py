from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, Service, ServiceReminder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ServiceSerializer(serializers.ModelSerializer):
    days_until_expiry = serializers.ReadOnlyField()
    days_until_payment_due = serializers.ReadOnlyField()
    is_expiring_soon = serializers.ReadOnlyField()
    is_payment_due_soon = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    status_color = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'vendor', 'service_name', 'start_date', 'expiry_date',
            'payment_due_date', 'amount', 'status', 'created_at', 'updated_at',
            'created_by', 'days_until_expiry', 'days_until_payment_due',
            'is_expiring_soon', 'is_payment_due_soon', 'is_overdue', 'status_color'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class VendorSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    active_services_count = serializers.ReadOnlyField()
    total_contract_value = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'status',
            'created_at', 'updated_at', 'created_by', 'services',
            'active_services_count', 'total_contract_value'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def validate_email(self, value):
        # Check if email is unique across all vendors
        if self.instance:
            if Vendor.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A vendor with this email already exists.")
        else:
            if Vendor.objects.filter(email=value).exists():
                raise serializers.ValidationError("A vendor with this email already exists.")
        return value
    
    def validate_name(self, value):
        # Check if name is unique
        if self.instance:
            if Vendor.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A vendor with this name already exists.")
        else:
            if Vendor.objects.filter(name=value).exists():
                raise serializers.ValidationError("A vendor with this name already exists.")
        return value


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'vendor', 'service_name', 'start_date', 'expiry_date',
            'payment_due_date', 'amount', 'status'
        ]
    
    def validate(self, data):
        # Validate that expiry date is after start date
        if data['expiry_date'] <= data['start_date']:
            raise serializers.ValidationError("Expiry date must be after start date.")
        
        # Validate that payment due date is after start date
        if data['payment_due_date'] <= data['start_date']:
            raise serializers.ValidationError("Payment due date must be after start date.")
        
        return data


class ServiceReminderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = ServiceReminder
        fields = [
            'id', 'service', 'reminder_type', 'reminder_date',
            'is_sent', 'sent_at', 'created_at'
        ]
        read_only_fields = ['created_at']


class VendorListSerializer(serializers.ModelSerializer):
    active_services_count = serializers.ReadOnlyField()
    total_contract_value = serializers.ReadOnlyField()
    
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'status',
            'created_at', 'updated_at', 'active_services_count', 'total_contract_value'
        ]


class ServiceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['status']
    
    def validate_status(self, value):
        valid_statuses = ['active', 'expired', 'payment_pending', 'completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value
