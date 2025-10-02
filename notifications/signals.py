from django.db.models.signals import post_save
from django.dispatch import receiver
from vendors.models import Service
from .tasks import check_expiring_services, check_payment_due_services


@receiver(post_save, sender=Service)
def service_post_save(sender, instance, created, **kwargs):
    """Trigger reminder checks when a service is created or updated"""
    if created or instance.status == 'active':
        # Check for expiring services
        check_expiring_services.delay()
        # Check for payment due services
        check_payment_due_services.delay()
