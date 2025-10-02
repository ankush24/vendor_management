from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from vendors.models import Service, ServiceReminder


@shared_task
def check_expiring_services():
    """Check for services expiring in the next 15 days and send reminders"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    # Find services expiring soon
    expiring_services = Service.objects.filter(
        expiry_date__range=[today, fifteen_days_later],
        status='active'
    ).select_related('vendor', 'created_by')
    
    for service in expiring_services:
        # Create reminder record
        reminder, created = ServiceReminder.objects.get_or_create(
            service=service,
            reminder_type='expiry',
            reminder_date=today,
            defaults={'is_sent': False}
        )
        
        if not created and not reminder.is_sent:
            # Send email reminder
            send_expiry_reminder.delay(service.id, reminder.id)


@shared_task
def check_payment_due_services():
    """Check for services with payment due in the next 15 days and send reminders"""
    today = timezone.now().date()
    fifteen_days_later = today + timedelta(days=15)
    
    # Find services with payment due soon
    payment_due_services = Service.objects.filter(
        payment_due_date__range=[today, fifteen_days_later],
        status__in=['active', 'payment_pending']
    ).select_related('vendor', 'created_by')
    
    for service in payment_due_services:
        # Create reminder record
        reminder, created = ServiceReminder.objects.get_or_create(
            service=service,
            reminder_type='payment',
            reminder_date=today,
            defaults={'is_sent': False}
        )
        
        if not created and not reminder.is_sent:
            # Send email reminder
            send_payment_reminder.delay(service.id, reminder.id)


@shared_task
def send_expiry_reminder(service_id, reminder_id):
    """Send expiry reminder email for a specific service"""
    try:
        service = Service.objects.get(id=service_id)
        reminder = ServiceReminder.objects.get(id=reminder_id)
        
        subject = f"Service Expiry Reminder: {service.service_name}"
        
        # Create email content
        context = {
            'service': service,
            'vendor': service.vendor,
            'days_until_expiry': service.days_until_expiry,
            'expiry_date': service.expiry_date,
        }
        
        # Send email to vendor contact and service creator
        recipients = [service.vendor.email, service.created_by.email]
        
        # Remove duplicates while preserving order
        recipients = list(dict.fromkeys(recipients))
        
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
        
        # Mark reminder as sent
        reminder.is_sent = True
        reminder.sent_at = timezone.now()
        reminder.save()
        
        return f"Expiry reminder sent for service {service.service_name}"
        
    except Service.DoesNotExist:
        return f"Service with id {service_id} not found"
    except ServiceReminder.DoesNotExist:
        return f"Reminder with id {reminder_id} not found"
    except Exception as e:
        return f"Error sending expiry reminder: {str(e)}"


@shared_task
def send_payment_reminder(service_id, reminder_id):
    """Send payment due reminder email for a specific service"""
    try:
        service = Service.objects.get(id=service_id)
        reminder = ServiceReminder.objects.get(id=reminder_id)
        
        subject = f"Payment Due Reminder: {service.service_name}"
        
        # Send email to vendor contact and service creator
        recipients = [service.vendor.email, service.created_by.email]
        
        # Remove duplicates while preserving order
        recipients = list(dict.fromkeys(recipients))
        
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
        
        # Mark reminder as sent
        reminder.is_sent = True
        reminder.sent_at = timezone.now()
        reminder.save()
        
        return f"Payment reminder sent for service {service.service_name}"
        
    except Service.DoesNotExist:
        return f"Service with id {service_id} not found"
    except ServiceReminder.DoesNotExist:
        return f"Reminder with id {reminder_id} not found"
    except Exception as e:
        return f"Error sending payment reminder: {str(e)}"


@shared_task
def daily_reminder_check():
    """Daily task to check for expiring services and payment due services"""
    check_expiring_services.delay()
    check_payment_due_services.delay()
    return "Daily reminder check completed"
