# Generated by Django 4.2.7 on 2023-12-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_mangement_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='average_response_time',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='fulfillment_rate',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='on_time_delivery_rate',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='quality_rating_avg',
        ),
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]