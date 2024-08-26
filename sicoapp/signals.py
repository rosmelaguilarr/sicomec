from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .utils import check_expirations
from .models import Driver, Notification, Vehicle

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    check_expirations()

@receiver(post_save, sender=Driver)
def update_or_remove_driver_notification(sender, instance, **kwargs):
    today = timezone.now().date()
    limit_date = today + timedelta(days=30)

    notifications = Notification.objects.filter(driver=f"{instance.name} {instance.last_name}")
    notifications.delete()

    if instance.expiration:
        try:
            expiration_date = instance.expiration.date()
        except AttributeError:
            expiration_date = None
        
        if expiration_date and today <= expiration_date <= limit_date:
            Notification.objects.create(
                license=instance.license,
                driver=f"{instance.name} {instance.last_name}",
                expiration=expiration_date.strftime('%Y-%m-%d'),
            )


@receiver(post_save, sender=Vehicle)
def update_or_remove_vehicle_notification(sender, instance, **kwargs):
    today = timezone.now().date()
    limit_date = today + timedelta(days=30)
    
    Notification.objects.filter(plate=instance.plate).delete()
    
    if instance.soat:
        try:
            soat_expiration =instance.soat + timedelta(days=365)
        except ValueError:
            soat_expiration = None
        
        if soat_expiration and today <= soat_expiration <= limit_date:
            Notification.objects.get_or_create(
                plate=instance.plate,
                name=instance.name,
                brand=instance.brand,
                soat=instance.soat,
            )
    
    if instance.citv:
        try:
            citv_expiration = instance.citv + timedelta(days=365)
        except ValueError:
            citv_expiration = None
        
        if citv_expiration and today <= citv_expiration <= limit_date:
            Notification.objects.get_or_create(
                plate=instance.plate,
                name=instance.name,
                brand=instance.brand,
                citv=instance.citv,
            )
