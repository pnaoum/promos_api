from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    """
    Health Checker endpoint for ELB or Docker usage
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={200: 'Ok'})
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

# @permission_classes((AllowAny,))
# @api_view(http_method_names=['GET'])
# def health_check(self, request, *args, **kwargs):
#     return Response(status=status.HTTP_200_OK)
