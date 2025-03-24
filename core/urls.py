from django.urls import path
from .views import homepage
from . import views


urlpatterns = [
    path('', homepage, name='home'),
    path('date-nights/', views.date_nights, name='date_nights'),
]




