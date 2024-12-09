from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentCreateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('comments/', CommentCreateView.as_view(), name='comment_create'),
]
