from password.encryption_util import decrypt
from . models import HassPermission, Password
from rest_framework import serializers
import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['id','name','password']
        extra_kwargs={'password': {'write_only':True,'required':True},'name': {'required':True}}

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
        return super(PasswordSerializer, self).validate(data)



class SharePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HassPermission
        fields = ['id','share_to','pass_id']
        extra_kwargs={'pass_id': {'required':True},'share_to': {'required':True}}
        