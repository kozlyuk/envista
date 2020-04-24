from rest_framework import serializers
from accounts.models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model details
    """
    class Meta:
        model = User
        fields = ['pk', 'email', 'mobile_number', 'first_name', 'last_name', 'password']
