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

    path('buy_order/create', views.buy_order_create_view, name='buy_order_create'),
    path('buy_order/update/<str:id>', views.buy_order_update_view, name='buy_order_update'),
    path('buy_order/list', views.buy_order_list_view, name='buy_order_list'),
    path('buy_order/delete/<str:id>', views.buy_order_delete_view, name='buy_order_delete'),

    path('fuel_order/create', views.fuel_order_create_view, name='fuel_order_create'),
    # path('fuel_order/update/<str:id>', views.fuel_order_update_view, name='fuel_order_update'),
    path('fuel_order/list', views.fuel_order_list_view, name='fuel_order_list'),
    path('fuel_order/generate_fuel_order_pdf/<str:id>', views.generate_fuel_order_pdf, name='generate_fuel_order_pdf'),
    path('fuel_order/delete/<str:id>', views.fuel_order_delete_view, name='fuel_order_delete'),
    path('fuel_order/control_card', views.control_card_view, name='control_card'),

    path('ballot/create', views.ballot_create_view, name='ballot_create'),
    path('ballot/update/<str:id>', views.ballot_update_view, name='ballot_update'),
    path('ballot/list_scheduled', views.ballot_list_scheduled_view, name='ballot_list_scheduled'),
    path('ballot/list_complete', views.ballot_list_complete_view, name='ballot_list_complete'),
    path('ballot/mark_return', views.ballot_mark_return_view, name='ballot_mark_return'),
    path('ballot/mark_return/update/<str:id>', views.update_return_datetime, name='update_return_datetime'),
    path('ballot/generate_ballot_pdf/<str:id>', views.generate_ballot_pdf, name='generate_ballot_pdf'),
    path('ballot/delete/<uuid:id>/', views.ballot_delete_view, name='ballot_delete'),
    
    path('notification/list', views.notification_list_view, name='notification_list'),
    path('notification/count', views.notification_count_view, name='notification_count'),
    path('notification/delete/<int:id>', views.notification_delete_view, name='notification_delete'),

    path('get_vehicle_details/<str:id>', views.get_vehicle_details_view, name='get_vehicle_details'),
    path('get_buy_order_details/<uuid:id_buy_order>', views.get_buy_order_details_view, name='get_buy_order_details'),
    path('get_fuel_orders/<uuid:id_buy_order>', views.get_fuel_orders_view, name='get_fuel_orders'),
    path('get_driver_details/<uuid:id>', views.get_driver_details_view, name='get_driver_details'),
]
