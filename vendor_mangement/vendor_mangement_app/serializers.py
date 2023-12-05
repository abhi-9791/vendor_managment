from rest_framework import serializers
from .models import Vendor,PurchaseOrder,HistoricalPerformance
class Vendor_Performance_Serializer(serializers.ModelSerializer):
    class Meta:
        model=HistoricalPerformance
        fields = '__all__'
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
