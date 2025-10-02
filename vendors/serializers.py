from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ServiceSerializer(serializers.ModelSerializer):
    days_until_expiry = serializers.ReadOnlyField()
    days_until_payment_due = serializers.ReadOnlyField()
    is_expiring_soon = serializers.ReadOnlyField()
    is_payment_due_soon = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'vendor', 'service_name', 'start_date', 'expiry_date',
            'payment_due_date', 'amount', 'status', 'created_at', 'updated_at',
            'created_by', 'days_until_expiry', 'days_until_payment_due',
            'is_expiring_soon', 'is_payment_due_soon'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class VendorSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'status',
            'created_at', 'updated_at', 'created_by', 'services'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def validate_email(self, value):
        # Make sure email is unique
        if self.instance:
            if Vendor.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This email is already in use by another vendor.")
        else:
            if Vendor.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use by another vendor.")
        return value
    
    def validate_name(self, value):
        # Make sure vendor name is unique
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
        # Check dates make sense
        if data['expiry_date'] <= data['start_date']:
            raise serializers.ValidationError("Expiry date must be after start date.")
        
        if data['payment_due_date'] <= data['start_date']:
            raise serializers.ValidationError("Payment due date must be after start date.")
        
        return data


class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'status',
            'created_at', 'updated_at'
        ]


class ServiceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['status']
    
    def validate_status(self, value):
        valid_statuses = ['active', 'expired', 'payment_pending', 'completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return value
