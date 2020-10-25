from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404, QueryDict
import requests

from auth0authorization.utils import get_user_info

from .models import Task
from .models import List
from boards.models import Board
from .serializers import TaskSerializer


class TaskCollection(APIView):
    def get(self, request, listId, format=None):
        response = get_user_info(request)
        try:
            list_check = List.objects.get(pk=listId)
            board_check = Board.objects.get(
                pk=list_check.board_id.pk, creatorEmail=response["email"]
            )
            tasks = Task.objects.filter(list_id=listId)
        except (List.DoesNotExist, Task.DoesNotExist):
            tasks = None
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
        # return Response(data={"message": "getting response"})

    def post(self, request, listId, format=None):
        response = get_user_info(request)
        email = response["email"]
        try:
            list_check = List.objects.get(pk=listId)
            board_check = Board.objects.get(
                pk=list_check.board_id.pk, creatorEmail=response["email"]
            )
        except (List.DoesNotExist, Board.DoesNotExist):
            board_check = None
        if board_check is not None:
            request.data["creatorEmail"] = email
            request.data["list_id"] = listId
            request.data["board_id"] = board_check.pk
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data={"message": "You do not have access to this board"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class TaskDetail(APIView):
    def get_object(self, pk, creatorEmail):
        try:
            return Task.objects.get(pk=pk, creatorEmail=creatorEmail)
        except Task.DoesNotExist:
            Http404

    def get(self, request, listId, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        task_obj = self.get_object(pk=pk, creatorEmail=creatorEmail)
        serializer = TaskSerializer(task_obj)
        return Response(serializer.data)

    def put(self, request, listId, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        task_obj = self.get_object(pk=pk, creatorEmail=creatorEmail)
        # put = QueryDict(request.body)
        # list_id_check = put.get("list_id")
        # if list_id_check is None:
        # request.data["list_id"] = listId
        request.data["creatorEmail"] = creatorEmail
        request.data["board_id"] = task_obj.board_id.pk
        serializer = TaskSerializer(task_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, listId, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        task_obj = self.get_object(pk=pk, creatorEmail=creatorEmail)
        task_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
