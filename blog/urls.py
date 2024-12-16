from django.urls import path
from .views import  (
    PostListCreateView, PostDetailView, CommentCreateView,
    index, post_detail
)

urlpatterns = [
    # مسیرهای API
    path('api/posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('api/comments/', CommentCreateView.as_view(), name='comment_create'),

    # مسیرهای HTML
    path('', index, name='index'),
    path('post/<int:id>/', post_detail, name='post_detail'),
]