from django.contrib.auth import authenticate
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import CustomUser
from .serializers import UserSerializer

# Create your views here.
class RegistraionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User created successfully!'},
                    status=status.HTTP_201_CREATED
                            )
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        # 1. Use get_object_or_404 to avoid crashing
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)

        # 2. Logic check
        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Perform the action
        request.user.following.add(user_to_follow)

        return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        if user_to_unfollow == self.request.user:
            return Response({'error': 'Cannot unfollow yourself'}, status.HTTP_400_BAD_REQUEST)

        self.request.user.following.remove(user_to_unfollow)
        return Response({'message' : f'You have unfollowed {user_to_unfollow.username}'})

