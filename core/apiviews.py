from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .utils import create_database_dict


class SetDatabaseFileView(APIView):
    def post(self, request):
        data_context = create_database_dict()
        return Response(data_context, status=status.HTTP_201_CREATED)
