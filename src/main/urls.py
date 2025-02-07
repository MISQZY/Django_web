from django.urls import path

from main.views import *

urlpatterns = [
    path('', main_page, name='home'),
    path('user/login/', user_login, name = 'login'),
    path('user/logout/', user_logout, name = 'logout'),
    path('user/profile/<str:username>/', user_profile, name='profile'),
]