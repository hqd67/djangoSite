import json
from django.http import JsonResponse
from .jwt_utils import verify_token

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/token"):
            return self.get_response(request)

        if request.path.startswith("/api/") and request.method != "GET":
            print("=== JWTMiddleware DEBUG ===")
            print("PATH:", request.path)
            try:
                for k, v in request.headers.items():
                    if k.lower().startswith("authorization") or k.lower().startswith("content"):
                        print(f"Header: {k} => {v}")
            except Exception as e:
                print("Error reading headers:", e)

            auth = request.headers.get("Authorization", "")
            if not auth:
                auth_meta = request.META.get("HTTP_AUTHORIZATION")
                print("HTTP_AUTHORIZATION (META):", auth_meta)
            else:
                print("Authorization header raw:", repr(auth))

            if not auth.startswith("Bearer "):
                print("-> No Bearer token found or wrong format")
                return JsonResponse({"error": "No token"}, status=401)

            token = auth.split()[1]
            print("-> token snippet:", token[:30], "len=", len(token))

            payload = verify_token(token, "access")
            if payload is None:
                print("-> token invalid or expired (verify_token returned None)")
                return JsonResponse({"error": "Invalid or expired token"}, status=401)

            print("-> token valid, payload:", payload)
            request.user_id = payload.get("user_id")

        return self.get_response(request)
