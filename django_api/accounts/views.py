from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_jwt.settings import api_settings
from .serializers import *
from .utils import *


# Create User View
@api_view(["POST"])
def create_user(request):
    # Serialize data, and only use data if verified
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        login_history = UserLoginHistory(
            user_id=serializer.validated_data["username"],
            ip_addr=request.META["REMOTE_ADDR"],
        )
        # Save login attempt
        login_history.save()

        # Call webhook to send POST notification
        send_hook(serializer.validated_data["username"], request.META["REMOTE_ADDR"])

        # Check if user has valid credentials and return user instance else None
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is not None:

            # Generate JWT token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"msg": "Credentials are not valid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
