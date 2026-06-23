from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ProgressPost, Comment
from .forms import ProgressPostForm


def feed(request):
    """
    Community feed showing all posts
    """
    posts = ProgressPost.objects.all()
    
    # Optional: filter posts by user
    user_filter = request.GET.get('user')
    if user_filter:
        posts = posts.filter(user__username=user_filter)
    
    return render(request, 'community/feed.html', {'posts': posts})


@login_required
def create_post(request):
    """
    Create a new progress post
    """
    if request.method == 'POST':
        form = ProgressPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Progress post created successfully!')
            return redirect('community:feed')
    else:
        form = ProgressPostForm()
    
    return render(request, 'community/create_post.html', {'form': form})


def post_detail(request, pk):
    """
    View a single post with comments
    """
    post = get_object_or_404(ProgressPost, pk=pk)
    return render(request, 'community/post_detail.html', {'post': post})


@login_required
def edit_post(request, pk):
    """
    Edit a post (only if user owns it)
    """
    post = get_object_or_404(ProgressPost, pk=pk)
    
    if post.user != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('community:feed')
    
    if request.method == 'POST':
        form = ProgressPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('community:post_detail', pk=post.pk)
    else:
        form = ProgressPostForm(instance=post)
    
    return render(request, 'community/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    """
    Delete a post (only if user owns it)
    """
    post = get_object_or_404(ProgressPost, pk=pk)
    
    if post.user != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('community:feed')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('community:feed')
    
    return render(request, 'community/delete_post.html', {'post': post})


@login_required
@require_POST
def like_post(request, pk):
    """
    Toggle like on a post (AJAX)
    """
    post = get_object_or_404(ProgressPost, pk=pk)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })


@login_required
@require_POST
def add_comment(request, pk):
    """
    Add a comment to a post
    """
    post = get_object_or_404(ProgressPost, pk=pk)
    content = request.POST.get('content')
    
    if content:
        Comment.objects.create(
            post=post,
            user=request.user,
            content=content
        )
        messages.success(request, 'Comment added!')
    else:
        messages.error(request, 'Comment cannot be empty.')
    
    return redirect('community:post_detail', pk=post.pk)