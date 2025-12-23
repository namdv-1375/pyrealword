from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ..serializers.auth_serializer import RegisterSerializer, LoginSerializer, UserDetailSerializer

class RegisterView(APIView):
  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']
      user = authenticate(username=username, password=password)
      
      if user is not None:
        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
      return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    return Response(UserDetailSerializer(request.user).data)
  
  def put(self, request):
    user = request.user
    data = request.data
    
    if 'email' in data:
      user.email = data['email']
    if 'first_name' in data:
      user.first_name = data['first_name']
    if 'last_name' in data:
      user.last_name = data['last_name']
    
    user.save()
    return Response(UserDetailSerializer(user).data)

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'user': UserDetailSerializer(user).data,
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }
