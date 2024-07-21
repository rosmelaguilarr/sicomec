from rest_framework import serializers
from .models import Driver, LicenseCategory, Vehicle

class LicenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseCategory
        fields = ['name']

class DriverSerializer(serializers.ModelSerializer):
    category = LicenseCategorySerializer()

    class Meta:
        model = Driver
        fields = ['name', 'last_name', 'license', 'category']  

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['plate','name','brand']  
