from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth #데이터베이스에서 유저 확인
from django.contrib.auth.models import User
from home import models as home_model
from home import forms
import datetime

def login(request):
    #POST 요청이 들어오면 로그인 처리
    if request.user.is_authenticated:
        return render(request, 'map.html', {'form': forms.TravelForm()})
    elif request.method == 'POST':
        user_name = request.POST['username']
        user_pw = request.POST['password']
        user = auth.authenticate(request, username=user_name, password=user_pw)
        if user is not None:
            auth.login(request, user)
            return redirect('map')
        else:
            return render(request, 'bad_login.html')
    #GET 요청이 들어오면 login form을 담고 있는 login html을 띄워주기
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['repeat']:
            # 회원가입
            new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            # 로그인
            auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            # 홈 리다이렉션
            return redirect('map')
    return render(request, 'register.html')

def schedule(request, travel_id):
    if request.method == 'POST':
        ride_form = forms.RideForm(request.POST)
        if ride_form.is_valid():
            ride = ride_form.save(commit=False)
            ride.schedule = home_model.Travel.objects.get(pk=travel_id)
            ride.save()
    rides = home_model.Ride.objects.filter(schedule__pk=travel_id).order_by('arriv_time')
    form = forms.RideForm()

    return render(request, 'schedule.html', {'travel_id': travel_id, 'rides': rides, 'form':form})

def status(request):
    curTravel = home_model.Travel.objects.filter(traveler__pk=request.user.id, start_date__lte=datetime.datetime.now(),
                                               arriv_date__gte=datetime.datetime.now()).first()
    if (curTravel == None):
        return render(request, 'no_car.html')
    else:
        return render(request, 'status.html', {'car':curTravel.car, 'travel_id': curTravel.id})

def userdetail(request):
    travels = home_model.Travel.objects.filter(traveler__pk=request.user.id)
    return render(request, 'userdetail.html', {'travels': travels})

def logout(request):
    auth.logout(request)
    return redirect('home')