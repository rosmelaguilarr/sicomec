from django.contrib import admin
from .models import Driver, Vehicle, FuelTap, Ballot, Notification, BuyOrder

admin.site.site_header = "Sistema Integral | SICOMEC"
admin.site.site_title = "SICOMEC"

class DriverAdmin(admin.ModelAdmin):
    list_display = ["dni","name","last_name","license","category","expiration","validity","available","user", "created"]
    readonly_fields = ('created',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ["plate","type","name","brand","chassis","model","production","fuel","mileage","hourometer","soat","citv","maintenance"  ,"user", "created"]
    readonly_fields = ('created',)

class FuelTapAdmin(admin.ModelAdmin):
    list_display = ["ruc","business_name","address","email","phone","user", "created"]
    readonly_fields = ('created',)

class BallotAdmin(admin.ModelAdmin):
    list_display = ["code","driver","drive_to", "plate", "vehicle_name","place","reason", "exit_date","return_date","user","created"]
    readonly_fields = ('created',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id","license","driver","expiration","plate","name","brand","soat","citv","created"]
    readonly_fields = ('created',)
    
class BuyOrderAdmin(admin.ModelAdmin):
    list_display = ["order","user_area","fueltap","fuel","stock","date","user","created"]
    readonly_fields = ('created',)


admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(FuelTap, FuelTapAdmin)
admin.site.register(Ballot, BallotAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(BuyOrder, BuyOrderAdmin)

