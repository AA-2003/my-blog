from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


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
    comments = post.comments.filter(parent__isnull=True)  # فقط کامنت‌های سطح اول

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # آیدی کامنت والد (در صورت وجود)

        if username and email and content:
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
            Comment.objects.create(
                post=post, parent=parent_comment, username=username, email=email, content=content
            )
            messages.success(request, 'کامنت یا پاسخ شما با موفقیت اضافه شد!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید.')

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