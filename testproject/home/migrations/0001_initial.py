# Generated by Django 4.1.5 on 2023-01-27 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('passNum', models.IntegerField()),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('availableStartDate', models.DateField()),
                ('availableEndDate', models.DateField()),
                ('cur_battery', models.IntegerField()),
                ('max_battery', models.IntegerField()),
                ('bedNum', models.IntegerField()),
                ('fridge', models.BooleanField()),
                ('mcwave', models.BooleanField()),
                ('tv', models.BooleanField()),
                ('booked', models.BooleanField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=200)),
                ('dest', models.CharField(max_length=200)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('arriv_date', models.DateField()),
                ('start_time', models.TimeField(default=django.utils.timezone.now)),
                ('arriv_time', models.TimeField()),
                ('travelerNum', models.IntegerField()),
                ('traveler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=200)),
                ('dest', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('arriv_time', models.DateTimeField()),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.travel')),
            ],
        ),
    ]
