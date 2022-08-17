from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.transactions import set_user_password
from news_letter.utils.exceptions.exceptions import AccessDeniedUser, DoesNotExistError
from users.tasks import _create_signaler_task
from users.tasks import send_email_confirm

User = get_user_model()


class RegisterEmailSerializer(serializers.ModelSerializer):
    """
    endpoint1:register_email user with email,password
    """
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value):
        norm_email = value.lower()
        user = User.soft_objects.get_publish(email=norm_email)
        if user is not None and user.is_active:
            raise AccessDeniedUser
        return norm_email

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.create_user(email=email, password=password)
        set_user_password(user=user, password=password)
        send_email_confirm.delay(email)

        return user


class NewsReporterEmailSerializer(serializers.ModelSerializer):
    """
    endpoint2:news_email with email,password
    """
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        norm_email = data['email'].lower()
        password = data['password']
        try:
            user = User.soft_objects.get_publish(email=norm_email)
            if user is not None and user.is_active and user.check_password(password):
                _create_signaler_task(norm_email)
            else:
                raise DoesNotExistError
        except User.DoesNotExist:
            raise DoesNotExistError

        return data
