from rest_framework import serializers
from password.encryption_util import decrypt
from password.models import OrgMember, OrgPassword, Organisation
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class createOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id','user','org_name']
        extra_kwargs={'org_name': {'required':True},'user':{'read_only':True}}

class OrgMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgMember
        fields = ['id','organisation','members']
        extra_kwargs={'members': {'required':True},'organisation':{'required':True}}


class AddOrgPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgPassword
        fields = ['id','organisation','name','password']
        extra_kwargs={'name': {'required':True},'password':{'write_only':True,'required':True},'organisation':{'required':True}}

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        representation['decrypt_pass'] = decrypt(instance.password)
        return representation

    def validate(self, data): 
        password = data.get('password')
        errors = dict() 
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)        
        if errors:
            raise serializers.ValidationError(errors)        
        return super(AddOrgPasswordSerializer, self).validate(data)