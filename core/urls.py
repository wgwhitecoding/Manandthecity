from django.urls import path
from .views import homepage
from . import views


urlpatterns = [
    path('', homepage, name='home'),
    path('date-nights/', views.date_nights, name='date_nights'),
    path('ex-files/', views.ex_files, name='ex_files'),
    path('love-heartbreak/', views.love_and_heartbreak, name='love_and_heartbreak'),

]




