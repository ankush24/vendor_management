from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from vendors.models import Service


@shared_task
def check_expiring_services():
    """Check for services expiring soon and send reminders"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    # Find services that expire in the next 15 days
    expiring_services = Service.objects.filter(
        expiry_date__range=[today, fifteen_days_later],
        status='active'
    ).select_related('vendor', 'created_by')
    
    for service in expiring_services:
        # Send email reminder directly
        send_expiry_reminder.delay(service.id)


@shared_task
def check_payment_due_services():
    """Check for services with payment due soon and send reminders"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    # Find services with payment due in the next 15 days
    payment_due_services = Service.objects.filter(
        payment_due_date__range=[today, fifteen_days_later],
        status__in=['active', 'payment_pending']
    ).select_related('vendor', 'created_by')
    
    for service in payment_due_services:
        # Send email reminder directly
        send_payment_reminder.delay(service.id)


@shared_task
def send_expiry_reminder(service_id):
    """Send email reminder for expiring service"""
    try:
        service = Service.objects.get(id=service_id)
        
        subject = f"Service Expiry Reminder: {service.service_name}"
        
        # Send email to vendor and creator
        recipients = [service.vendor.email, service.created_by.email]
        recipients = list(dict.fromkeys(recipients))  # Remove duplicates
        
        message = f"""
Dear {service.vendor.contact_person},

This is a reminder that the service "{service.service_name}" for vendor "{service.vendor.name}" 
is expiring in {service.days_until_expiry} days on {service.expiry_date}.

Please take necessary action to renew or extend the service.

Service Details:
- Service Name: {service.service_name}
- Vendor: {service.vendor.name}
- Start Date: {service.start_date}
- Expiry Date: {service.expiry_date}
- Amount: ${service.amount}

Best regards,
Vendor Management System
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            recipient_list=recipients,
            fail_silently=False,
        )
        
        return f"Expiry reminder sent for service {service.service_name}"
        
    except Service.DoesNotExist:
        return f"Service with id {service_id} not found"
    except Exception as e:
        return f"Error sending expiry reminder: {str(e)}"


@shared_task
def send_payment_reminder(service_id):
    """Send email reminder for payment due"""
    try:
        service = Service.objects.get(id=service_id)
        
        subject = f"Payment Due Reminder: {service.service_name}"
        
        # Send email to vendor and creator
        recipients = [service.vendor.email, service.created_by.email]
        recipients = list(dict.fromkeys(recipients))  # Remove duplicates
        
        message = f"""
Dear {service.vendor.contact_person},

This is a reminder that payment for the service "{service.service_name}" for vendor "{service.vendor.name}" 
is due in {service.days_until_payment_due} days on {service.payment_due_date}.

Please ensure payment is processed before the due date.

Service Details:
- Service Name: {service.service_name}
- Vendor: {service.vendor.name}
- Start Date: {service.start_date}
- Payment Due Date: {service.payment_due_date}
- Amount: ${service.amount}

Best regards,
Vendor Management System
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            recipient_list=recipients,
            fail_silently=False,
        )
        
        return f"Payment reminder sent for service {service.service_name}"
        
    except Service.DoesNotExist:
        return f"Service with id {service_id} not found"
    except Exception as e:
        return f"Error sending payment reminder: {str(e)}"


@shared_task
def daily_reminder_check():
    """Run daily checks for expiring and payment due services"""
    check_expiring_services.delay()
    check_payment_due_services.delay()
    return "Daily reminder check completed"
