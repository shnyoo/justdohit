from django.shortcuts import render, get_object_or_404
from .forms import TravelForm, RideForm
from .models import Vehicle, Ride, Travel
import requests
import time

def home(request):
    return render(request, 'index.html')

def map(request):
    form = TravelForm()
    return render(request, 'map.html', {'form':form})

def search(request):
    if request.method == 'GET':
        form = TravelForm(request.GET)
        request.session['start'] = form['start'].value()
        request.session['dest'] = form['dest'].value()
        request.session['start_date'] = form['start_date'].value()
        request.session['arriv_date'] = form['arriv_date'].value()
        request.session['travelerNum'] = form['travelerNum'].value()

        if (form.is_valid):
            cars = Vehicle.objects.filter(availableStartDate__lte=form['start_date'].value(),
                                          availableEndDate__gte=form['arriv_date'].value(),
                                          booked=False)
        return render(request, 'search.html', {'form':form, 'cars': cars})

def reserve(request):
    return render(request, 'reserve.html')

def confirm(request):
    if request.method == 'POST':
        bookedVehicle = Vehicle.objects.get(id=request.session['car_id'])
        if (bookedVehicle.booked == True):
            message = '이미 예약된 차량입니다.'
            return render(request, 'error.html', {'message':message})
        else:
            final_form = TravelForm({'start':request.session['start'],
                                    'dest':request.session['dest'],
                                    'start_date':request.session['start_date'],
                                    'arriv_date':request.session['arriv_date'],
                                    'travelerNum':request.session['travelerNum']
                                    })
            if (final_form.is_valid):
                final = final_form.save(commit=False)
                final.start_time = request.POST['start_time']
                final.arriv_time = request.POST['arriv_time']
                final.car = bookedVehicle
                final.traveler = request.user
                final.save()
                
                bookedVehicle.booked = True
                bookedVehicle.save()

                first_ride_form = RideForm({'dest':final.start, 'arriv_time':final.start_time})
                if (first_ride_form.is_valid()):
                    first_ride = first_ride_form.save(commit=False)
                    first_ride.schedule = final
                    first_ride.save()
        
                next_ride_form = RideForm({'dest':final.dest, 'arriv_time':final.arriv_time})
                if (next_ride_form.is_valid()):
                    next_ride = next_ride_form.save(commit=False)
                    next_ride.schedule = final
                    print(next_ride)
                    next_ride.save()

                return render(request, 'confirm.html', {'start':final.start, 'travel_id':final.id,
                                                        'start_date':final.start_date, 'start_time':final.start_time})
    else:
        message = '잘못된 접근입니다.'
        return render(request, 'error.html', {'message':message})

def detail(request, car_id):
    request.session['car_id'] = car_id
    car_detail = get_object_or_404(Vehicle, pk=car_id)
    return render(request, 'detail.html', {'car_detail': car_detail})