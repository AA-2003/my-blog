from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


@csrf_exempt  # برای ساده‌تر شدن کار، فرم نیازی به امنیت CSRF ندارد
@login_required  # مطمئن می‌شود که کاربر لاگین کرده است
def add_post(request):
    if not request.user.is_superuser:
        return redirect('post_list') # پیام خطا
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # پشتیبانی از فایل‌ها
        if form.is_valid():
            form.save()
            return redirect('post_list')  # تغییر مسیر به لیست پست‌ها
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # فیلتر کردن کامنت‌های تاییدشده
    comments = Comment.objects.filter(post=post, is_approved=True, parent=None).order_by('-created_at')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        content = request.POST['content']
        parent_id = request.POST.get('parent_id')

        parent = Comment.objects.get(id=parent_id) if parent_id else None
        new_comment = Comment(post=post, parent=parent, username=username, email=email, content=content)
        new_comment.save()

        messages.success(request, "نظر شما ثبت شد و منتظر تایید ادمین است.")
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


@staff_member_required
def manage_comments(request):
    comments = Comment.objects.filter(is_approved=False).order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action')
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)

        if action == 'approve':
            comment.is_approved = True
            comment.save()
            messages.success(request, "کامنت تایید شد.")
        elif action == 'delete':
            comment.delete()
            messages.success(request, "کامنت حذف شد.")

        return redirect('manage_comments')

    return render(request, 'blog/manage_comments.html', {'comments': comments})