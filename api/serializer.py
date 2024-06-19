from django.contrib.auth.models import User
from .models import Tutorial
from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



class TutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutorial
        fields = ['tutorialNo','title','content']


