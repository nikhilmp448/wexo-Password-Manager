from rest_framework import serializers
from user.models import Account
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ('id','username','email','is_active','password')
        extra_kwargs={'email':{'write_only':False,'required':True},'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account(
                email=validated_data['email'],
                username=validated_data['username'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
