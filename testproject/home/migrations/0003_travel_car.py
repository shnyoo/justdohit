# Generated by Django 4.1.5 on 2023-01-28 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_ride_start_remove_ride_start_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.vehicle'),
        ),
    ]