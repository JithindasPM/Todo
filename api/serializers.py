from rest_framework import serializers
from work.models import *
from rest_framework.authtoken.models import Token

class User_Registration_Serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password','first_name','last_name']
        read_only_fields=['id']
    
    def create(self,validated_data):

        return User.objects.create_user(**validated_data)
    
class Todo_Serializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Taskmodel
        fields='__all__'
        read_only_fields=['id','created_date','user','completed']

        

# class Token_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model=Token
#         fields='__all__'


