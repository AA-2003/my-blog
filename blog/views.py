from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


@csrf_exempt  # برای ساده‌تر شدن کار، فرم نیازی به امنیت CSRF ندارد
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # پشتیبانی از فایل‌ها
        if form.is_valid():
            form.save()
            return redirect('post_list')  # تغییر مسیر به لیست پست‌ها
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required  # مطمئن می‌شود که کاربر لاگین کرده است
def add_post(request):
    # بررسی اینکه آیا کاربر ادمین اصلی است
    if not request.user.is_superuser:
        return redirect('post_list') # پیام خطا

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(title=title, content=content)
            return redirect('post_list')
    return render(request, 'blog/add_post.html')

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