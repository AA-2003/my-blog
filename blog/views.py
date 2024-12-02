from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_superuser

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required  
@user_passes_test(is_admin)
def add_post(request):
    if not request.user.is_superuser:
        return redirect('post_list') 
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('post_list') 
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})


# @login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, is_approved=True, parent=None).order_by('-created_at')
    
    if request.method == 'POST':
        content = request.POST['content']
        parent_id = request.POST.get('parent_id')

        # Use the logged-in user's data
        username = request.user.username
        email = request.user.email

        parent = Comment.objects.get(id=parent_id) if parent_id else None
        new_comment = Comment(post=post, parent=parent, username=username, email=email, content=content, is_approved=True)
        new_comment.save()

        return redirect('post_detail', post_id=post_id)

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})



@login_required
def delete_post(request, post_id):
    # دریافت پست یا بازگشت 404 اگر موجود نباشد
    post = get_object_or_404(Post, id=post_id)
    
    # اطمینان از اینکه کاربر ادمین است
    if not request.user.is_staff:  # یا هر چک دیگری برای محدودیت دسترسی
        return HttpResponseForbidden("شما اجازه حذف این پست را ندارید.")

    post.delete()  # حذف پست
    messages.success(request, "پست با موفقیت حذف شد.")
    return redirect('post_list')        