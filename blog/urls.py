from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('add/', views.add_post, name='add_post'),  # آدرس صفحه افزودن پست
    path('<int:post_id>/', views.post_detail, name='post_detail'),  # آدرس صفحه جزئیات
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('manage-comments/', views.manage_comments, name='manage_comments'),
]
