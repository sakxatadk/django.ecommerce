from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_products, name = 'all_products'),
    path('create/', views.product_create, name = 'product_create'),
    path('<int:product_id>/edit/', views.product_edit, name = 'product_edit'),
    path('<int:product_id>/delete/', views.product_delete, name = 'product_delete'),
    path('register/', views.register, name='register'),
    
]
