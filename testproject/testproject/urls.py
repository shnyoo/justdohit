from django.contrib import admin
from django.urls import path
from home import views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('map/', views.map, name="map"),

    path('search/', views.search, name="search"),
    path('detail/<int:car_id>', views.detail, name="detail"),
    path('reserve/', views.reserve, name="reserve"),
    path('confirm/', views.confirm, name="confirm"),

    path('userdetail/', accounts_views.userdetail, name="userdetail"),
    path('schedule/<int:travel_id>', accounts_views.schedule, name="schedule"),
    path('status/', accounts_views.status, name="status"),

    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout, name='logout')
]