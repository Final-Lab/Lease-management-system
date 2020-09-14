from django.urls import path
from . import views

app_name = 'Rent'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('', views.test, name='home'),      #tempoary modified for test
    path('logout/', views.mylogout, name='logout'),
    path('apply/', views.apply_for_provider, name='apply'),
    
    path('supplier/',views.apply_for_provider,name='apply_supplier'),
    path('rented/<int:user_id>',views.check_rented_items,name='check_rented_items'),
    path('<int:user_id>/<str:request_type>',views.check_all_requests,name='check_requests'),
    path('<int:user_id>/',views.user_info,name='user_info'),
]
