from django.contrib import admin
from django.urls import path
from Core import views

urlpatterns = [
    path('', views.inventario, name='inventario'),
    path('productos/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('admin/', admin.site.urls),
]
