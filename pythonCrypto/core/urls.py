from django.urls import path
from .views import index, current_price

app_name = 'core'

urlpatterns = [
    path('', index, name='home'),
    path('current_price', current_price, name='current_price')
]
