from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views import View
from django.utils.html import linebreaks
from django.db.models import Q
from django.http import JsonResponse
from .models import Post
from django.contrib.auth.decorators import login_required
import stripe
import re




# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


# --------------------------
# Individual Blog Post Detail
# --------------------------


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Split content into paragraphs using 2+ newlines
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', post.content) if p.strip()]

    # Get related images by position
    images_by_position = {img.position: img for img in post.images.all()}

    # Create blocks for template
    content_blocks = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        content_blocks.append({'type': 'text', 'content': linebreaks(paragraph)})
        if idx in images_by_position:
            content_blocks.append({'type': 'image', 'image': images_by_position[idx], 'position': idx})

    return render(request, 'posts/detail.html', {
        'post': post,
        'content_blocks': content_blocks
    })




# --------------------------
# Stripe Tease Page
# --------------------------
def tease(request):
    return render(request, 'posts/tease.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })


# --------------------------
# Stripe Checkout View
# --------------------------
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


# --------------------------
# Intimate Edit Tab (X-rated)
# --------------------------
def intimate_edit(request):
    # Only show X-rated premium content (category = 'intimate')
    premium_posts = Post.objects.filter(is_premium=True, category='intimate').order_by('-date')
    return render(request, 'posts/intimate_edit.html', {'premium_posts': premium_posts})



# --------------------------
# Subscriber Exclusives Tab (All Premium Posts)
# --------------------------
@login_required
def subscriber_exclusives(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    premium_posts = Post.objects.filter(is_premium=True).order_by('-date')
    return render(request, 'posts/subscriber_exclusives.html', {
        'premium_posts': premium_posts
    })




# --------------------------
# Search View (Accessible to All)
# --------------------------
def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(intro__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-date')

    return render(request, 'posts/search_results.html', {
        'query': query,
        'results': results,
    })
