from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from .serializers import EntrySerializer, UserSerializer
from rest_framework import status
from .models import Entry
from django.contrib.auth.models import User
from craiyon import Craiyon
from PIL import Image
from io import BytesIO

# Create your views here.


class EntriesListView(APIView):
    def get(self, request):
        queryset = Entry.objects.all()
        
        serializer = EntrySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EntrySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response()


class EntriesDetailView(APIView):
    def get(self, request, id):
        entry = Entry.objects.filter(id=id).first()
        serializer = EntrySerializer(entry)
        entry_data = serializer.data

        return Response(entry_data)

    # def put(self, request):

        
    #     return Response()

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
        return Response()


class UserDetailView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class DreamImagesView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass