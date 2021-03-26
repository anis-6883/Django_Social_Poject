from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm
from App_Login.models import *
from .models import Post, Like
from django.contrib.auth.decorators import login_required

@login_required
def home_page(request):

    follwer_user = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=follwer_user.values_list('following'))

    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)

    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)
    context = {
        'search' : search,
        'result' : result,
        'posts' : posts,
        'liked_post_list' : liked_post_list
    }
    return render(request, 'App_Post/index.html', context)

@login_required
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your Post Uploded Successfully...✅")
            return redirect('profile_page')
    context = {
        'form' : form
    }
    return render(request, 'App_Post/post_create.html', context)


@login_required
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your Post Updated Successfully...✅")
            return redirect('profile_page')
    context = {
        'form' : form
    }
    return render(request, 'App_Post/post_create.html', context)


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.warning(request, "Your Post Deleted Successfully...✅")
    return redirect('profile_page')


@login_required
def post_liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return redirect('home')


@login_required
def post_unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return redirect('home')
