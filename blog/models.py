from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)  # عنوان پست
    content = models.TextField()  # متن پست
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # آپلود عکس
    video = models.FileField(upload_to='videos/', blank=True, null=True)  # آپلود ویدئو
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # ارتباط با مدل Post
    username = models.CharField(max_length=100)  # نام کاربری
    email = models.EmailField()  # ایمیل
    content = models.TextField()  # متن کامنت
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد

    def __str__(self):
        return f"{self.username} - {self.content[:20]}"