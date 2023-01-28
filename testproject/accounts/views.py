from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth #데이터베이스에서 유저 확인
from django.contrib.auth.models import User
from home import models as home_model
from home import forms

def login(request):
    #POST 요청이 들어오면 로그인 처리
    if request.method == 'POST':
        user_name = request.POST['username']
        user_pw = request.POST['password']
        user = auth.authenticate(request, username=user_name, password=user_pw)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'bad_login.html')

    #GET 요청이 들어오면 login form을 담고 있는 login html을 띄워주기
    else:
        return render(request, 'login.html')

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
    return render(request, 'status.html')

def userdetail(request):
    travels = home_model.Travel.objects.filter(traveler__pk=request.user.id)
    return render(request, 'userdetail.html', {'travels': travels})

def logout(request):
    auth.logout(request)
    return redirect('home')