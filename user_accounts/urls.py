from django.urls import path
from . import views

app_name = 'user_accounts'

urlpatterns = [
    path('settings/', views.user_settings, name='settings'),
]



