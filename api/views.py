import uuid
from google.cloud import storage
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from .serializers import DreamImageSerializer, EntrySerializer, UserSerializer
from rest_framework import status
from .models import Entry, DreamImage
from django.contrib.auth.models import User
from craiyon import Craiyon
from PIL import Image
from io import BytesIO
from .wombo_service import send_task_to_dream_api
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import json


# Create your views here.


class EntryListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        queryset = Entry.objects.select_related('image_id')
        user_id = request.query_params.get("user_id")

        if user_id:  # user id
            queryset.filter(created_by=user_id)

        serializer = EntrySerializer(queryset, many=True)
        print(serializer.data)

        entries = serializer.data

        for i in range(len(entries)):
            entries[i]['id'] = str(entries[i]['id'])
            entries[i]['image_id'] = str(entries[i]['image_id'])

        return Response(entries)

    def post(self, request):
        # Create the image in the database

        # image_id
        dream_image_data = {"url": request.data["url"]}
        serializer = DreamImageSerializer(data=dream_image_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        dream_image = serializer.save()

        entry_data = request.data
        entry_data['created_by'] = request.user.id
        entry_data['image_id'] = dream_image.id
        # Create the entry
        serializer = EntrySerializer(data=entry_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response()


class EntryDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        entry = Entry.objects.filter(id=id).first()
        serializer = EntrySerializer(entry)
        entry_data = serializer.data

        return Response(entry_data)

    # def put(self, request):

    #     return Response()


class UserListView(APIView):  # registration view
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        # print(request.data)
        # data = json.loads(request.data)
        # print(data)

        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user: User = serializer.save()
        token = Token.objects.create(user=user)

        return Response(
            {
                'token': token.key,
                'user': serializer.data
            },
            status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = []
    # permission_classes = [IsAuthenticated]
    permission_classes = []

    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data['id'] = str(user_data['id'])

        return Response(user_data)


class DreamImagesView(APIView):
    """
    Creates a set of images based on a prompt, and returns nine images, and uploads to database
    """

    def post(self, request):
        prompt = request.data['prompt']
        if not prompt:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        DAYDREAM_STYLE = 39

        send_task_to_dream_api(DAYDREAM_STYLE, prompt)

        client = storage.Client.from_service_account_json(
            json_credentials_path='woven-nova-376821-f6f1803e9106.json')

        bucket = client.get_bucket('hackuci2023')

        object_name_in_gcs_bucket = bucket.blob(f'{uuid.uuid1()}.jpg')

        object_name_in_gcs_bucket.upload_from_filename('image.jpg')
        public_url = object_name_in_gcs_bucket.public_url

        return Response({"url": public_url})


class DreamImageDetailView(APIView):
    def get(self, request, id):
        image = DreamImage.objects.filter(id=id).first()
        serializer = DreamImageSerializer(image)
        data = serializer.data

        data['id'] = str(data['id'])

        return Response(data)


class TokenView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):  # creates a token and returns the token
        if not request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=request.user)

        return Response({"token": token.key, 'user_id': str(request.user.id)})
