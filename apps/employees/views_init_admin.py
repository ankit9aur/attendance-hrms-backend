from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([AllowAny])
def create_superuser_once(request):
    secret = request.data.get("secret")

    # CHANGE THIS STRING
    if secret != "INIT_ADMIN_123":
        return Response({"error": "Unauthorized"}, status=403)

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response({"error": "username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    User.objects.create_superuser(
        username=username,
        password=password,
        email=email,
    )

    return Response({"status": "superuser created"})
