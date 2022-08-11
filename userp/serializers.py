
from lib2to3.pgen2 import token
from xml.dom import ValidationErr
from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','date_of_birth','tc','password','password2']
        extra_kwargs={
            'passsword':{'write_only':True}
        }
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password !=password2:
            raise serializers.ValidationError("Password and conform password doen't match")
        return attrs
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name','date_of_birth']
        
class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, min_length=4,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255, min_length=4,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2'] 
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password !=password2:
            raise serializers.ValidationError("Password and conform password doen't match")
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token',token)
            link='http://localhost:3000/user/'+uid+'/'+token
            print('Password Reset Link', link)
            return attrs
            
        else:
            raise ValidationErr('You are not a Register User')
        
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, min_length=4,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255, min_length=4,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2'] 
        
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password !=password2:
                raise serializers.ValidationError("Password and conform password doen't match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('Toke is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
            
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationErr('Token is not valid or Expired')
        
    
    
        