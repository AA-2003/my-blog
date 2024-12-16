from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import render
from django.http import HttpResponseNotFound
import requests

def index(request):
    return render(request, 'blog/index.html')

def post_detail(request, id):
    API_URL = f"http://127.0.0.1:8000/api/posts/{id}/"  
    token = request.user.auth_token.key
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            post = response.json()
            return render(request, 'blog/postDetail.html', {'post': post})
        elif response.status_code == 403:
            return HttpResponseNotFound("You do not have permission to view this post.") 
        else:
            return HttpResponseNotFound("Post not found.")
    except requests.exceptions.RequestException:
        return HttpResponseNotFound("Error connecting to API.")


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        print("GET method is called")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("POST method is called")
        return super().post(request, *args, **kwargs)
    
class PostDetailView(generics.RetrieveDestroyAPIView):
    print(2)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
