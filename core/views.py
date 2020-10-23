from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse


class TestResponse(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return JsonResponse(data={"test_response": "works"})
