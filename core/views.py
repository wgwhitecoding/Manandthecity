from django.shortcuts import render
from posts.models import Post
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def homepage(request):
    public_posts = Post.objects.filter(is_premium=False).order_by('-date')[:6]
    premium_posts = Post.objects.filter(is_premium=True).order_by('-date')[:3]
    return render(request, 'core/homepage.html', {
        'posts': public_posts,
        'premium_teasers': premium_posts,
    })




