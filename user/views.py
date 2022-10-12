from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import Account
from user.serializers import UserSerializer
from rest_framework import status
# Create your views here.

class UserListViewSet(viewsets.ViewSet):
    
    def list(self,request):
        queryset = Account.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)



class UserRegisterViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

