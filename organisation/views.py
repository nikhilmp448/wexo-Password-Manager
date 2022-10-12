from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from organisation.permissions import IsOwnerOrMember
from organisation.serializers import AddOrgPasswordSerializer, OrgMemberSerializer, createOrganisationSerializer
from rest_framework.decorators import action
from password import encryption_util
from password.models import OrgMember, OrgPassword, Organisation
from django.db.models import Q
from rest_framework import serializers

# Create your views here.
class OrganisationViewSet(viewsets.ViewSet):
    
    queryset = Organisation.objects.all()
    serializer_class = createOrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer=createOrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def list(self,request):

        curent_user = self.request.user
        queryset = Organisation.objects.filter(user = curent_user)
        serializer = createOrganisationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Organisation.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = createOrganisationSerializer(obj)       
        return Response(serializer.data)
    
    def destroy(self, request, pk) :
        queryset = Organisation.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response({'detail':'Organisation deleted successfully'},status=status.HTTP_200_OK)


class Org_Members(viewsets.ViewSet):
    queryset = OrgMember.objects.all()
    serializer_class = OrgMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        org_memb = OrgMember.objects.filter(organisation=self.request.data['organisation'],members=self.request.data['members']).first()
        serializer=OrgMemberSerializer(data=request.data)
        if serializer.is_valid():
            if org_memb:
                raise serializers.ValidationError({"message":"member is already in group"})
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        curent_user = self.request.user
        queryset = OrgMember.objects.filter(Q(members = curent_user) | Q(organisation__user = curent_user))
        serializer = OrgMemberSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk) :
        queryset = Organisation.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response({'detail':'member removed successfully'},status=status.HTTP_200_OK)

    
class Org_Password(viewsets.ViewSet):
    queryset = OrgPassword.objects.all()
    serializer_class = AddOrgPasswordSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrMember]

    def create(self, request):
        serializer=AddOrgPasswordSerializer(data=request.data)
        if serializer.is_valid():
            enc_password=encryption_util.encrypt(serializer.validated_data['password'])
            serializer.save(password=enc_password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        vlaue = OrgMember.objects.filter(members=self.request.user)
        result=[]
        if vlaue.exists :
            for i in range(len(vlaue.values())):
                result.append(vlaue.values()[i]['organisation_id'])
        print(result)


        queryset = OrgPassword.objects.filter(Q(organisation__in = result)|Q(organisation__user = request.user))
        serializer = AddOrgPasswordSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = OrgPassword.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = AddOrgPasswordSerializer(obj)       
        return Response(serializer.data)

    def update(self, request, pk = None):
        queryset = OrgPassword.objects.all()
        obj=get_object_or_404(queryset,id=pk)
        serializer = AddOrgPasswordSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        enc_pass = encryption_util.encrypt(serializer.validated_data['password'])
        serializer.save(password = enc_pass)
            
        return Response(serializer.data)
