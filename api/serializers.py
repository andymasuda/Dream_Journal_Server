from rest_framework.serializers import ModelSerializer
from .models import Entry, DreamImage
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data=validated_data)
        


class DreamImageSerializer(ModelSerializer):
    class Meta:
        model = DreamImage
        fields = '__all__'
