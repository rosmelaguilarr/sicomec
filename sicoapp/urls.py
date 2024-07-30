from django.urls import path
from . import views

app_name = 'sicomec'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('driver/create', views.driver_create_view, name='driver_create'),
    path('driver/update/<str:id>', views.driver_update_view, name='driver_update'),
    path('driver/list', views.driver_list_view, name='driver_list'),
    path('driver/delete/<str:id>', views.driver_delete_view, name='driver_delete'),

    path('vehicle/create', views.vehicle_create_view, name='vehicle_create'),
    path('vehicle/update/<str:id>', views.vehicle_update_view, name='vehicle_update'),
    path('vehicle/list', views.vehicle_list_view, name='vehicle_list'),
    path('vehicle/delete/<str:id>', views.vehicle_delete_view, name='vehicle_delete'),

    path('fueltap/create', views.fueltap_create_view, name='fueltap_create'),
    path('fueltap/update/<str:id>', views.fueltap_update_view, name='fueltap_update'),
    path('fueltap/list', views.fueltap_list_view, name='fueltap_list'),
    path('fueltap/delete/<str:id>', views.fueltap_delete_view, name='fueltap_delete'),

    path('ballot/create', views.ballot_create_view, name='ballot_create'),
    path('ballot/update/<str:id>', views.ballot_update_view, name='ballot_update'),
    path('ballot/list_scheduled', views.ballot_list_scheduled_view, name='ballot_list_scheduled'),
    path('ballot/list_complete', views.ballot_list_complete_view, name='ballot_list_complete'),
    path('ballot/mark_return', views.ballot_mark_return_view, name='ballot_mark_return'),
    path('ballot/mark_return/update/<str:id>', views.update_return_datetime, name='update_return_datetime'),
    path('ballot/generate_ballot_pdf/<str:id>', views.generate_ballot_pdf, name='generate_ballot_pdf'),
    path('ballot/delete/<uuid:id>/', views.ballot_delete_view, name='ballot_delete'),

    path('search_driver_by_dni/', views.search_driver_by_dni, name='search_driver_by_dni'),
    path('search_vehicle_by_plate/', views.search_vehicle_by_plate, name='search_vehicle_by_plate'),
]
