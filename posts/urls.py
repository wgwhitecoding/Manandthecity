from django.urls import path
from . import views
from .views import CreateCheckoutSessionView


urlpatterns = [
    path('subscribe/tease/', views.tease, name='subscribe_tease'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('intimate-edit/', views.intimate_edit, name='intimate_edit'),
    path('subscriber-exclusives/', views.subscriber_exclusives, name='subscriber_exclusives'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]









