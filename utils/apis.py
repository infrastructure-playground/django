from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def uptime(request):
    """
    Initially used for Stackdriver Uptime Check
    """
    return Response({"message": "Uptime Check Ok"})


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Initially used for GCP Load Balancer Health Check
    """
    return Response({"message": "Health Check Ok"})
