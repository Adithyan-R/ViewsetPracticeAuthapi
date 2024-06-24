from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tutorial, Comment
from .serializer import TutorialSerializer, RegisterUserSerializer, LoginSerializer, CommentSerializer
from django.contrib.auth.models import User

# Create your views here.

class RegisterApi(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterUserSerializer(data= data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class LoginApi(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class TutorialList(viewsets.ReadOnlyModelViewSet):
    serializer_class = TutorialSerializer
    def get_queryset(self):
        return Tutorial.objects.all()



class TutorialViewset(viewsets.ModelViewSet):

    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer