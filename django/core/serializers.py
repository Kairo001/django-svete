"""Serializadores de la app core."""

# RestFramework
from dataclasses import fields
from rest_framework.serializers import ModelSerializer

# Modelos
from core.models import User

class UserSerializer(ModelSerializer):
    """Serializador para el modelo User"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance