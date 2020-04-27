from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from accounts.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model details
    """
    groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['pk',
                  'email',
                  'mobile_number',
                  'first_name',
                  'last_name',
                  'groups',
                  'is_active',
                  'password',
                  ]
        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = False
        return super(UserDetailsSerializer, self).create(validated_data)
