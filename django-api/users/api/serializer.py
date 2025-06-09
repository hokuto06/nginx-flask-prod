from rest_framework import serializers
from users.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','email','username','password','password2','is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'default': False},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data        

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')        
        is_staff = validated_data.pop('is_staff', False)

        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']