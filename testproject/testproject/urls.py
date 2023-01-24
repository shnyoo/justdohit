from django.contrib import admin
from django.urls import path
import home.views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.views.home, name="메인"),

    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout, name='logout')
]