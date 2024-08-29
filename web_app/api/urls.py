from django.urls import path # type: ignore
from . import views

urlpatterns = [
    #cada vez que llegue un request para una pagina vacia ("") va a redirigir a pagina main
    path("dashboard", views.index, name = "api-index"),
    path("staff/", views.staff, name = "api-staff"),
    path("staff/detail/<int:pk>/", views.staff_detail, name = "api-staff-detail"),
    path("productos/", views.productos, name = "api-productos"),
    path("ordenes/", views.ordenes, name = "api-ordenes"),
    path("ordenes/detail/<int:pk>/", views.order_detail, name='api-ordenes-detail'),
    path('ordenes/edit/<int:pk>/', views.order_edit, name='api-ordenes-edit'),
    path("staff_ordenes/detail/<int:pk>/", views.staff_order_detail, name='api-staff-ordenes-detail'),
    path('staff_ordenes/edit/<int:pk>/', views.staff_order_edit, name='api-staff-ordenes-edit'),
    path('get_product_quantity/<int:product_id>/', views.get_product_quantity, name='get_product_quantity'),
    path("productos/delete/<int:pk>/", views.product_delete, name = "api-productos-delete"),
    path("productos/update/<int:pk>/", views.product_update, name = "api-productos-update"),
    
]
 