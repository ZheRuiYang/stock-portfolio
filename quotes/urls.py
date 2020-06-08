from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('add_delete_stock', views.add_delete_stock, name='add_delete_stock'),
    path('delete/<stock_id>', views.delete, name='delete')
]
