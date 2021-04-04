import json

from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import shutil
from . import db
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import BackendSerializer
from .models import Backend
import base64
import cv2

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class UserView(APIView):

    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))
        user = {}
        user['name'] = data.get('name')
        user['email'] = data.get('email')
        user['password'] = data.get('password')
        if user['name'] and user['email'] and user['password']:
            response = db.signup(user)
            if response == "Email Exists":
                return Response({'result': 'failure'}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
        else:
            response = db.login(user)
            if response == "No such email exists":
                return Response({'result': response}, status=status.HTTP_200_OK)
            elif response == "Wrong Password":
                return Response({'result': response}, status=status.HTTP_200_OK)
            else:
                return Response({'result': response}, status=status.HTTP_200_OK)


class ProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        project = {}
        project['action'] = data.get('action', None)
        project['email'] = data.get('email')
        project['name'] = data.get('name')
        project['description'] = data.get('description')
        project['worktypes'] = data.get('worktypes')
        project['contractors'] = data.get('contractors')
        project['users'] = data.get('users')
        project['_id'] = data.get('id')
        # project['image'] = data.get('image')
        if project['action'] == "Add":
            res = db.addProject(project)
            if res is not None:
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'failure'}, status=status.HTTP_200_OK)
        elif project['action'] == "GET":
            res = db.get_projects(email=project['email'])
            print(res)
            if res is not None:
                return Response({'result': res}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'Failure'}, status=status.HTTP_200_OK)
        elif project['action'] == "GET_BY_ID":
            res = db.get_projects(id=project['_id'])
            print(res)
            if res is not None:
                return Response({'result': res}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'Failure'}, status=status.HTTP_200_OK)
        elif project['action'] == "GET_IMAGE_BY_ID":
            res = db.get_images(project_id=project['_id'])
            print(res)
            if res is not None:
                return Response({'result': res}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'Failure'}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        Image = {}
        image = request.data['file']
        image_type = request.data['type']
        Image['id'] = request.data['id']
        Backend.objects.create(image=image)
        with open(os.path.join(BASE_DIR, f'media\\post_images\\{image}'), "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        Image['image'] = f"data:{image_type};base64," + my_string.decode('utf-8')
        res = db.addImage(Image)
        if res is not None:
            shutil.rmtree(os.path.join(BASE_DIR, 'media\\post_images'))
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'result': 'failure'}, status=status.HTTP_200_OK)
