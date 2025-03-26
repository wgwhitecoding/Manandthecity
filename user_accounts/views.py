from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.contrib import messages
from core.models import Subscription
from .models import Profile
import os

@login_required
def user_settings(request):
    subscription = getattr(request.user, 'subscription', None)

    # Prevent unsubscribed users from accessing the page
    if not subscription or not subscription.is_active:
        messages.error(request, "You must be subscribed to access your settings.")
        return redirect('posts:subscribe_tease')

    # Ensure the user has a profile with a default avatar
    profile, created = Profile.objects.get_or_create(user=request.user)
    if not profile.avatar:
        profile.avatar = 'avatar9.png'
        profile.save()

    # Load avatar images dynamically from /static/avatars/
    avatar_dir = finders.find('avatars')
    avatar_choices = sorted(os.listdir(avatar_dir)) if avatar_dir else []

    if request.method == 'POST':
        avatar = request.POST.get('avatar')
        if avatar in avatar_choices:
            profile.avatar = avatar
            profile.save()
            messages.success(request, "Avatar updated successfully!")
            return redirect('user_accounts:settings')

    context = {
        'subscription': subscription,
        'avatar_choices': avatar_choices,
        'current_avatar': profile.avatar,
        'username': request.user.username,
        'hide_search': True
    }
    return render(request, 'user_accounts/settings.html', context)

