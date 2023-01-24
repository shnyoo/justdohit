from django.shortcuts import render, redirect
from django.contrib import auth #데이터베이스에서 유저 확인
from django.contrib.auth.models import User

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


def logout(request):
    auth.logout(request)
    return redirect('home')