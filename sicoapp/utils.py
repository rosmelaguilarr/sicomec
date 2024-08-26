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
        if vehicle.soat: 
            soat_expiration = vehicle.soat + timedelta(days=365) 
            if today <= soat_expiration <= limit_date: 
                Notification.objects.get_or_create(
                    plate=vehicle.plate,
                    name=vehicle.name,
                    brand=vehicle.brand,
                    soat=vehicle.soat,
                )

        if vehicle.citv:  
            citv_expiration = vehicle.citv + timedelta(days=365)  
            if today <= citv_expiration <= limit_date:  
                
                Notification.objects.get_or_create(
                    plate=vehicle.plate,
                    name=vehicle.name,
                    brand=vehicle.brand,
                    citv=vehicle.citv,
                )

