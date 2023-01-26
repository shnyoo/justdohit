from django.contrib import admin
from django.urls import path
from home import views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('map/', views.map, name="map"),

    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout, name='logout')
]