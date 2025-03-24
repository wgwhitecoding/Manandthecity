from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from .models import Post
import stripe

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# View for single blog post
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Redirect if trying to access premium content without login
    if post.is_premium and not request.user.is_authenticated:
        return redirect('subscribe_tease')

    return render(request, 'posts/detail.html', {'post': post})

# Tease page if user not logged in
def tease(request):
    return render(request, 'posts/tease.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })

# Stripe checkout session view
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'unit_amount': 500,  # £5.00
                    'product_data': {
                        'name': 'The Intimate Edit – Monthly Subscription',
                    },
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/accounts/signup/'),
            cancel_url=request.build_absolute_uri('/'),
        )
        return JsonResponse({'id': session.id})





