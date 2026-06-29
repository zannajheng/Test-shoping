from django.urls import path
from apps.service import views

urlpatterns = [
    path('service/', views.service, name='service'),
    path('admin/service/', views.admin_sercice, name='admin_service'),
    path('admin/service/reading/', views.admin_reading),
    path('admin/service/reading/send/',views.admin_reading_send),
    path('service/face/', views.face),
    path('admin/order/update/', views.admin_order_update_status, name='admin_order_update_status'),
]
