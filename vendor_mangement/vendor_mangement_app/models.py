
from django.db import models
from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()
        return on_time_deliveries / total_completed_pos if total_completed_pos > 0 else 0.0
    def calculate_quality_rating_avg(self):
        completed_pos_with_rating = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        return completed_pos_with_rating.aggregate(average_rating=Coalesce(Avg('quality_rating'), 0.0))['average_rating']
    def calculate_average_response_time(self):
        completed_pos_with_acknowledgment = self.purchaseorder_set.filter(status='completed',acknowledgment_date__isnull=False)
        total_completed_pos = completed_pos_with_acknowledgment.count()
        if total_completed_pos > 0:
            total_response_time = sum(
                (po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_acknowledgment
            )
            return total_response_time / total_completed_pos
        return 0.0
    def calculate_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.count()
        if total_pos > 0:
            successful_fulfillments = self.purchaseorder_set.filter(status='completed', issues__isnull=True).count()
            return successful_fulfillments / total_pos
        return 0.0
    # def update_historical_performance(self):
    #     # Save historical performance data
    #     HistoricalPerformance.objects.create(
    #         vendor=self,
    #         date=timezone.now(),
    #         on_time_delivery_rate=self.calculate_on_time_delivery_rate(),
    #         quality_rating_avg=self.calculate_quality_rating_avg(),
    #         average_response_time=self.calculate_average_response_time(),
    #         fulfillment_rate=self.calculate_fulfillment_rate(),
    #     )

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    # items=models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    def acknowledge_order(self):
        self.acknowledgment_date =Vendor.calculate_average_response_time()
        self.save()
   
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
