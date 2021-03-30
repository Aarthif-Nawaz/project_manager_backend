import json

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from . import db


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

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        project = {}
        project['action'] = data.get('action')
        project['email'] = data.get('email')
        project['name'] = data.get('name')
        project['description'] = data.get('description')
        project['worktypes'] = data.get('worktypes')
        project['contractors'] = data.get('contractors')
        project['users'] = data.get('users')
        if project['action'] == "Add":
            res = db.addProject(project)
            if res is not None:
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'failure'}, status=status.HTTP_200_OK)
        elif project['action'] == "GET":
            res = db.get_projects(project['email'])
            print(res)
            if res is not None:
                return Response({'result': res}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'Failure'}, status=status.HTTP_200_OK)


