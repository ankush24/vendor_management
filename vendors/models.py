from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils import timezone
from datetime import timedelta


class Vendor(models.Model):
    """Represents a vendor/company we work with"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_vendors')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
    
    def __str__(self):
        return self.name
    


class Service(models.Model):
    """Represents a service/contract with a vendor"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('payment_pending', 'Payment Pending'),
        ('completed', 'Completed'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)
    start_date = models.DateField()
    expiry_date = models.DateField()
    payment_due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_services')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        unique_together = ['vendor', 'service_name', 'start_date']
    
    def __str__(self):
        return f"{self.vendor.name} - {self.service_name}"
    
    @property
    def days_until_expiry(self):
        """Get number of days until expiry"""
        today = timezone.now().date()
        return (self.expiry_date - today).days
    
    @property
    def days_until_payment_due(self):
        """Get number of days until payment due"""
        today = timezone.now().date()
        return (self.payment_due_date - today).days
    
    @property
    def is_expiring_soon(self):
        """Check if service expires within 15 days"""
        return self.days_until_expiry <= 15 and self.days_until_expiry >= 0
    
    @property
    def is_payment_due_soon(self):
        """Check if payment is due within 15 days"""
        return self.days_until_payment_due <= 15 and self.days_until_payment_due >= 0
    
    def save(self, *args, **kwargs):
        """Auto-update status based on dates when saving"""
        today = timezone.now().date()
        if self.expiry_date < today and self.status == 'active':
            self.status = 'expired'
        elif self.payment_due_date < today and self.status == 'active':
            self.status = 'payment_pending'
        super().save(*args, **kwargs)

