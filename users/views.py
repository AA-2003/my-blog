from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    permission_classes = [AllowAny]  # اجازه دسترسی عمومی

    def get(self, request):
        """بازگشت یک فرم ساده برای ورود"""
        return Response(
            {
                "message": "Please provide 'username' and 'password' to log in.",
                "example": {
                    "username": "your_username",
                    "password": "your_password",
                },
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """بررسی اطلاعات کاربری و ورود"""
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            return Response(
                {"message": f"Welcome, {user.username}!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Handle logout for GET requests
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logged out successfully!'}, status=200)
        return Response({'message': 'No active session to log out from.'}, status=400)

    def post(self, request):
        # Handle logout for POST requests
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({'message': 'Logged out successfully!'}, status=200)
        return Response({'message': 'No active session to log out from.'}, status=400)