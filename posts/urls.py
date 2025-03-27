from django.urls import path
from . import views
from .views import CreateCheckoutSessionView

app_name = 'posts'

urlpatterns = [
    path('subscribe/tease/', views.tease, name='subscribe_tease'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('intimate-edit/', views.intimate_edit, name='intimate_edit'),
    path('subscriber-exclusives/', views.subscriber_exclusives, name='subscriber_exclusives'),
    path('comment/<int:comment_id>/like/', views.toggle_like, name='toggle_like'),
    path('search/', views.search, name='search'),

    # Comment actions
    path('<slug:slug>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('<slug:slug>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<slug:slug>/reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),  # ✅ This fixed

    # Post detail must come last
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]











