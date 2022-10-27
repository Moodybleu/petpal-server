from rest_framework import serializers
from .models import Pet, User
from django.contrib.auth.hashers import make_password

# function to hash password
def validate_password(self, value: str) -> str:
    '''
    hashed value passed by user

    :paramvalue: user password
    :return: hashed pw
    '''
    return make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email','password')

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'name', 'breed', 'date_of_birth', 'nickname', 'catchphrase','user')