from django.urls import path
from . import views

app_name = 'Rent'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.mylogout, name='logout'),
    path('apply/', views.apply_for_provider, name='apply'),

]