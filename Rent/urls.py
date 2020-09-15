from django.urls import include, path
from . import views

app_name = 'Rent'
urlpatterns = [
    path('register/', include([
        path('', views.register_page),
        path('page/', views.register_page),
        path('sendCode/', views.register_get_code),
        path('confirm/', views.register_confirm),
    ])),
    path('login/', views.my_login, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('user/supplier', views.apply_for_supplier, name='apply'),
    path('rent/<int:item_id>', views.apply_for_item, name='rent'),
    path('supplier/add/', views.apply_add_item, name='rent'),
    path('supplier/<int:user_id>/edit/<int:item_id>', views.edit_item, name='rent'),
    path('supplier/<int:user_id>/return/<int:item_id>', views.return_rented_item, name='rent'),
    path('<int:user_id>/check/<int:req_id>/<str:action>', views.check_item_application, name='rent'),
    path('rented/<int:user_id>', views.check_rented_items, name='check_rented_items'),
    path('<int:user_id>/requests/<str:request_type>', views.check_all_requests, name='check_requests'),
    path('<int:user_id>/info', views.user_info, name='user_info'),
]
