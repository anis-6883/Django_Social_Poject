from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from App_Post.models import Post


def register_page(request):
    form = RegisterForm(request.POST or None)
    required_form = RequiredForm(request.POST or None)
    if form.is_valid() and required_form.is_valid():
        user = form.save()
        profile = required_form.save(commit=False)
        profile.user = user
        profile.save()
        # user_profile = Profile()
        # user_profile.user = user
        # user_profile.save()
        messages.success(request, "Your account has created successfully!")
        return redirect('login_page')
    context = {
        'form' : form,
        'required_form' : required_form
    }
    return render(request, 'App_Login/register.html', context)


def login_page(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully')
            return redirect('home')
        else:
            messages.warning(request, 'Your Username or Password is invalid!❌')

    context = {
    'form' : form
    }
    return render(request, 'App_Login/login.html', context)

@login_required
def logout_page(request):
    messages.success(request, 'Logout Successfully. Log In Again...')
    logout(request)
    return redirect('login_page')


@login_required
def change_password(request):
    current_user = request.user
    form = PasswordChangeForm(current_user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Your Password Have Changed...✅ Login Again")
        return redirect('profile_page')

    context = {
        'form' : form
    }
    return render(request, 'App_Login/change_password.html', context)


@login_required
def profile_page(request):
    posts = Post.objects.all()
    context = {'posts' : posts}
    return render(request, 'App_Login/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
        request.FILES,
        instance=request.user.user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile has Updated...✅')
            return redirect('profile_page')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'App_Login/edit_profile.html', context)


@login_required
def other_profile(request, username):
    user_obj = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_obj)
    if user_obj == request.user:
        return redirect('profile_page')
    context = {
        'user_obj' : user_obj,
        'already_followed' : already_followed
    }
    return render(request, 'App_Login/other_profile.html', context)


@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('other_profile', kwargs={'username' : username}))


@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('other_profile', kwargs={'username' : username}))