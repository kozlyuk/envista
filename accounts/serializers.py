from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from accounts.models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model details
    """
    class Meta:
        model = User
        fields = ['pk',
                  'email',
                  'mobile_number',
                  'first_name',
                  'last_name',
                  'password']

    def create(self, validated_data):
        User.objects.create_user(
            password=make_password(validated_data['user'].pop('password')),
            **validated_data.pop('user')
        )
