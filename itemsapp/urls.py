from django.urls import path
from .views import * # Import/Change as per need 


urlpatterns = [
    path ('items/', ItemsView),
    path('item/<int:nm>/', ItemView),
    ]  # Add URL & Views as per need