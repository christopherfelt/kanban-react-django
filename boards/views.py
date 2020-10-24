from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
import requests

from auth0authorization.utils import get_user_info

from .models import Board
from .serializers import BoardSerializer


class BoardList(APIView):
    def get(self, request, format=None):
        response = get_user_info(request)
        try:
            boards = Board.objects.filter(creatorEmail=response["email"])
        except Board.DoesNotExist:
            boards = None
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response = get_user_info(request)
        request.data["creatorEmail"] = response["email"]
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetail(APIView):
    def get_object(self, pk, creatorEmail):
        try:
            return Board.objects.get(pk=pk, creatorEmail=creatorEmail)
        except Board.DoesNotExist:
            Http404

    def get(self, request, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        board = self.get_object(pk=pk, creatorEmail=creatorEmail)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        board = self.get_object(pk=pk, creatorEmail=creatorEmail)
        request.data["creatorEmail"] = creatorEmail
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        response = get_user_info(request)
        creatorEmail = response["email"]
        board = self.get_object(pk=pk, creatorEmail=creatorEmail)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
