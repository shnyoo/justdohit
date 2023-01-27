from django.shortcuts import render, get_object_or_404
from .forms import TravelForm
from .models import Vehicle, Ride, Travel
import requests

def home(request):
    return render(request, 'index.html')

def map(request):
    form = TravelForm()
    return render(request, 'map.html', {'form':form})

def search(request):
    if request.method == 'GET':
        form = TravelForm(request.GET)
        if (form.is_valid):
            cars = Vehicle.objects.filter(availableStartDate__lte=form['start_date'].value(),
                                          availableEndDate__gte=form['arriv_date'].value(),
                                          booked=False)
        return render(request, 'search.html', {'form':form, 'cars': cars})

def reserve(request):
    return render(request, 'reserve.html')

def confirm(request):
    return render(request, 'confirm.html')

def detail(request, post_id):
    car_detail = get_object_or_404(Vehicle, pk=post_id)
    return render(request, 'detail.html', {'car_detail': car_detail})