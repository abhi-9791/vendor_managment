from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vendor_mangement_app.models import *
from vendor_mangement_app.serializers import VendorSerializer,PurchaseSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count, Avg
from .serializers import Vendor_Performance_Serializer


class VendorListView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorDetailView(APIView):
    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class PurchaseListView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = PurchaseSerializer(vendors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseOrderDetailView(APIView):
    def get(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
        serializer = PurchaseSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
        serializer = PurchaseSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        performance_data = {
            'vendor':vendor,
            'date':vendor.calculate_on_time_delivery_rate(),
            'on_time_delivery_rate': vendor.calculate_on_time_delivery_rate(),
            'quality_rating_avg': vendor.calculate_quality_rating_avg(),
            'average_response_time': vendor.calculate_average_response_time(),
            'fulfillment_rate': vendor.calculate_fulfillment_rate(),
        }
        serializer = Vendor_Performance_Serialize(performance_data)
        serializer.save()
        return Response(serializer.data)
class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.acknowledge_order()
        return Response({'message': 'Purchase order acknowledged successfully.'})




    