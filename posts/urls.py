from django.urls import path
from . import views
from .views import CreateCheckoutSessionView


urlpatterns = [
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('subscribe/tease/', views.tease, name='subscribe_tease'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
]








