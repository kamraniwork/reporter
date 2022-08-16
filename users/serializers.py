from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterEmailSerializer(serializers.ModelSerializer):
    """
    Register user with email,password
    """
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ('email', 'password')
