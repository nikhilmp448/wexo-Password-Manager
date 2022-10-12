from rest_framework import permissions
from password.models import HassPermission, OrgMember, Organisation
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class IsOwnerOrMember(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    edit_methods = ("PUT","PATCH","GET")

    # def has_permission(self , request ,view , obj):
    #     pass


    def has_object_permission(self, request, view, obj):
       
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        try:
            org_member = OrgMember.objects.filter(members = request.user).first()
            if org_member is None:
                return obj.organisation.user == request.user
        except:
            pass

        return (org_member.members == request.user and request.method not in self.edit_methods) or obj.organisation.user == request.user

