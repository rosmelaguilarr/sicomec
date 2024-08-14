from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Driver, Vehicle, Notification

def check_expirations():
    today = timezone.now().date()
    limit_date = today + timedelta(days=30)
    
    drivers = Driver.objects.filter(expiration__lte=limit_date, expiration__gte=today)
    for driver in drivers:
        full_name = f"{driver.name} {driver.last_name}"
        
        Notification.objects.get_or_create(
            license=driver.license,
            driver=full_name,
            expiration=driver.expiration,
            
        )

    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        soat_expiration = vehicle.soat + timedelta(days=365)
        citv_expiration = vehicle.citv + timedelta(days=365)
        
        if soat_expiration <= limit_date and soat_expiration >= today:
            Notification.objects.get_or_create(
                plate=vehicle.plate,
                name=vehicle.name,
                brand=vehicle.brand,
                soat=vehicle.soat,
            )
        
        if citv_expiration <= limit_date and citv_expiration >= today:
            Notification.objects.get_or_create(
                plate=vehicle.plate,
                name=vehicle.name,
                brand=vehicle.brand,
                citv=vehicle.citv,
            )