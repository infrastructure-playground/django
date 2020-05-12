from django.contrib.auth.models import User
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


@api_view(['GET'])
@permission_classes([AllowAny])
def delete_test_registered_user(request):
    user = User.objects.filter(username=f"UI_{request.GET['platform']}_test")
    if user.exists():
        user.delete()
        return Response({"message": "Delete Test Registered User Success"})
    return Response({"message": "User does not exist yet"})
