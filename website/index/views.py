from django.shortcuts import render, redirect
from django.contrib import messages
from community.models import UserAsking, Comment
from django.contrib.auth.models import User


def index(request):
    request.session['switch_comment'] = False
    return render(request, 'index/index.html')


def about_us(request):
    return render(request, 'index/about-us.html')


def user_api(request):
    if request.user.is_authenticated:
        return redirect('api:ask-api-view')
    else:
        messages.warning(request, 'you have to login to be able to access this page',
                         extra_tags='user-api-warning')
        return redirect('accounts:login')
