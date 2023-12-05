from django.contrib import admin
from .models import Vendor,HistoricalPerformance,PurchaseOrder
admin.site.register([Vendor,HistoricalPerformance,PurchaseOrder])
