from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password_confirmation = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'password_confirmation', 'first_name', 'last_name']
    extra_kwargs = {
      'first_name': {'required': False},
      'last_name': {'required': False},
    }

  def validate(self, attrs):
    if attrs['password'] != attrs['password_confirmation']:
      raise serializers.ValidationError({"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    validated_data.pop('password_confirmation')
    user = User.objects.create_user(**validated_data)
    return user


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name']
