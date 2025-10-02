from django.db.models.signals import post_save
from django.dispatch import receiver
from vendors.models import Service
from .tasks import check_expiring_services, check_payment_due_services


@receiver(post_save, sender=Service)
def service_post_save(sender, instance, created, **kwargs):
    """Run reminder checks when a service is saved"""
    if created or instance.status == 'active':
        # Check if we need to send any reminders
        check_expiring_services.delay()
        check_payment_due_services.delay()
