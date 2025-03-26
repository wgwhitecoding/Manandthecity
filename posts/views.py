from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views import View
from django.utils.html import linebreaks
from django.db.models import Q
from django.http import JsonResponse
from .models import Post
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm
from django.contrib import messages
from django.views.decorators.http import require_POST
import stripe
import re


from django.contrib import messages



# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# --------------------------
# Individual Blog Post Detail
# --------------------------

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Fetch all comments for this post, including replies
    all_comments = Comment.objects.filter(post=post).select_related('user').prefetch_related('replies').order_by('created_at')
    top_level_comments = all_comments.filter(parent__isnull=True)

    # Only allow commenting if user is authenticated AND subscribed
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = (
            hasattr(request.user, 'subscription') and
            request.user.subscription.is_active
        )

    # Handle comment form (top-level comment only)
    if request.method == 'POST' and is_subscribed:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts:post_detail', slug=slug)
    elif is_subscribed:
        form = CommentForm()
    else:
        form = None

    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': top_level_comments,
        'form': form,
        'is_subscribed': is_subscribed,
    })


# ------------------------------
# comment edit deletePost Detail
# ------------------------------
@require_POST
@login_required
def edit_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    body = request.POST.get("body", "").strip()
    if body:
        comment.body = body
        comment.save()
    return redirect('posts:post_detail', slug=slug)



@require_POST
@login_required
def delete_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('posts:post_detail', slug=slug)






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

@login_required
def reply_to_comment(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    parent_comment = get_object_or_404(Comment, id=comment_id, post=post)

    # Only allow replies if user is subscribed
    if not hasattr(request.user, 'subscription') or not request.user.subscription.is_active:
        return redirect('posts:post_detail', slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, initial={'parent': parent_comment.id})
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.parent = parent_comment  # 👈 attach reply to parent
            reply.save()
            return redirect('posts:post_detail', slug=slug)
        
    elif request.method == 'POST':
        messages.error(request, "Something went wrong with your reply.")

    return redirect('posts:post_detail', slug=slug)

