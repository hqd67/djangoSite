from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password

from .models import User
from .jwt_utils import create_access_token, create_refresh_token, verify_token


@csrf_exempt
def get_tokens(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    body = json.loads(request.body)
    email = body.get("email")
    password = body.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    if not check_password(password, user.hashed_password):
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    return JsonResponse({
        "access": access,
        "refresh": refresh
    })


@csrf_exempt
def refresh_access_token(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    body = json.loads(request.body)
    refresh = body.get("refresh")

    payload = verify_token(refresh, "refresh")
    if payload is None:
        return JsonResponse({"error": "Invalid refresh token"}, status=400)

    new_access = create_access_token(payload["user_id"])

    return JsonResponse({"access": new_access})
