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
                  'password',
                  'is_active'
                  ]
        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = False
        return super(UserDetailsSerializer, self).create(validated_data)
