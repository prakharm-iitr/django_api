from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .utils import *

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


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
        username = serializer.validated_data["username"]
        login_hist = UserLoginHistory(
            user_id=username, ip_addr=request.META["REMOTE_ADDR"],
        )
        # Save login attempt
        login_hist.save()

        # Call webhook to send POST notification
        send_hook(username, request.META["REMOTE_ADDR"])

        # Check if user has valid credentials and return user instance else None
        user = authenticate(
            username=username, password=serializer.validated_data["password"],
        )

        if user is not None:
            refresh = RefreshToken.for_user(User.objects.get(username=username))

            return Response(
                {"token": str(refresh.access_token)}, status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def register_new(request):
#
#     try:
#         User.objects.get(username=request.data["username"])
#         return Response(
#             {"username": request.data["username"], "msg": "Username already exists"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#         # raise ValidationError("Username already exists")
#     except ObjectDoesNotExist:
#         user = User(
#             username=request.data["username"],
#         )
#         user.save()
#
#     return Response({"username": user.username}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def history_view(request, user_id):

    if not request.user.is_staff and not user_id == request.user.username:
        return Response(
            {"msg": "You are unauthorised to access the resource"}, status=status.HTTP_401_UNAUTHORIZED
        )

    history = UserLoginHistory.objects.filter(user_id=user_id)
    if not history:
        return Response(
            {"msg": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    response_data = {
        "user": user_id,
        "history": [{obj.ip_addr: obj.time.strftime("%X %x")} for obj in history],
    }

    return Response(response_data, status=status.HTTP_200_OK)
