from django.apps import apps
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([AllowAny])
def truncate_all_tables(request):
    secret = request.data.get("secret")

    if secret != "NUKE_DB_123":
        return Response({"error": "Unauthorized"}, status=403)

    for model in apps.get_models():
        model.objects.all().delete()

    return Response({"status": "ALL DATA DELETED"})
