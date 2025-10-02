from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils import timezone
from datetime import timedelta


class Vendor(models.Model):
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
    
    @property
    def active_services_count(self):
        return self.services.filter(status='active').count()
    
    @property
    def total_contract_value(self):
        return sum(service.amount for service in self.services.filter(status='active'))


class Service(models.Model):
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
        today = timezone.now().date()
        return (self.expiry_date - today).days
    
    @property
    def days_until_payment_due(self):
        today = timezone.now().date()
        return (self.payment_due_date - today).days
    
    @property
    def is_expiring_soon(self):
        return self.days_until_expiry <= 15 and self.days_until_expiry >= 0
    
    @property
    def is_payment_due_soon(self):
        return self.days_until_payment_due <= 15 and self.days_until_payment_due >= 0
    
    @property
    def is_overdue(self):
        today = timezone.now().date()
        return (self.expiry_date < today or self.payment_due_date < today) and self.status == 'active'
    
    @property
    def status_color(self):
        if self.is_overdue:
            return 'red'
        elif self.is_expiring_soon or self.is_payment_due_soon:
            return 'orange'
        elif self.status == 'completed':
            return 'green'
        else:
            return 'blue'
    
    def save(self, *args, **kwargs):
        # Auto-update status based on dates
        today = timezone.now().date()
        if self.expiry_date < today and self.status == 'active':
            self.status = 'expired'
        elif self.payment_due_date < today and self.status == 'active':
            self.status = 'payment_pending'
        super().save(*args, **kwargs)


class ServiceReminder(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=[
        ('expiry', 'Expiry Reminder'),
        ('payment', 'Payment Due Reminder'),
    ])
    reminder_date = models.DateField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['service', 'reminder_type', 'reminder_date']
    
    def __str__(self):
        return f"{self.service} - {self.reminder_type} - {self.reminder_date}"