from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
import requests

from auth0authorization.utils import get_user_info

from .models import List
from boards.models import Board
from .serializers import ListSerializer


class ListCollection(APIView):
    def get(self, request, boardId, format=None):
        response = get_user_info(request)
        try:
            lists = List.objects.filter(
                creatorEmail=response["email"], board_id=boardId
            )
        except List.DoesNotExist:
            lists = None
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def post(self, request, boardId, format=None):
        response = get_user_info(request)
        email = response["email"]
        try:
            board_access = Board.objects.get(pk=boardId, creatorEmail=email)
        except Board.DoesNotExist:
            board_access = None
        if board_access is not None:
            request.data["creatorEmail"] = email
            request.data["board_id"] = boardId
            serializer = ListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data={"message": "You do not have access to this board"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ListDetail(APIView):
    def get_object(self, pk, creatorEmail):
        try:
            return List.objects.get(pk=pk, creatorEmail=creatorEmail)
        except List.DoesNotExist:
            Http404

    def get(self, request, boardId, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        board = self.get_object(pk=pk, creatorEmail=creatorEmail)
        serializer = ListSerializer(board)
        return Response(serializer.data)

    def put(self, request, boardId, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        list_obj = self.get_object(pk=pk, creatorEmail=creatorEmail)
        request.data["creatorEmail"] = creatorEmail
        request.data["board_id"] = boardId
        serializer = ListSerializer(list_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, boardId, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        list_obj = self.get_object(pk=pk, creatorEmail=creatorEmail)
        list_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
