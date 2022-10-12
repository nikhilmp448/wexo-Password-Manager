from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from password import encryption_util
from .serializers import PasswordSerializer, SharePasswordSerializer
from .models import HassPermission, Password
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.


class MyPasswordViewSet(viewsets.ModelViewSet):
    """
    Password
    """
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self,request):
        serializer=PasswordSerializer(data=request.data)
        if serializer.is_valid():
            enc_password=encryption_util.encrypt(serializer.validated_data['password'])
            serializer.save(user=self.request.user,password=enc_password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self,request):
        curent_user = self.request.user
        queryset = Password.objects.filter(user = curent_user)
        serializer = PasswordSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = Password.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = PasswordSerializer(obj)       
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        enc_pass = encryption_util.encrypt(serializer.validated_data['password'])
        serializer.save(password = enc_pass)
            
        return Response(serializer.data)   


class sharePassword(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def create(self , request):
        serializer=SharePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sharedPassword(viewsets.ViewSet):
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self,request):
        vlaue = HassPermission.objects.filter(Q(share_to=self.request.user))
        result=[]
        if vlaue.exists :
            for i in range(len(vlaue.values())):
                result.append(vlaue.values()[i]['pass_id_id'])
        print(result)

        queryset = Password.objects.filter(id__in = result)
        serializer = PasswordSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Password.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = PasswordSerializer(obj)       
        return Response(serializer.data)

    def update(self, request, pk = None):
        queryset = Password.objects.all()
        obj=get_object_or_404(queryset,id=pk)
        serializer = PasswordSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        enc_pass = encryption_util.encrypt(serializer.validated_data['password'])
        serializer.save(password = enc_pass)
            
        return Response(serializer.data)



