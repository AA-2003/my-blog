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
