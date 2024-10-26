from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from api import exceptions
from api.auth.token.serializers import TokenCreateSerializer, TokenRefreshSerializer
from api.permissions import AllowAny


class TokenCreateView(jwt_views.TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenCreateSerializer

    def post(self, request, *args, **kwargs):
        # create an instance of the serializer
        serializer = self.get_serializer(
            data=request.data  # pass the data the user supplied
        )

        #  if this isnt run - the `validated_data` field will not be available
        serializer.is_valid(
            raise_exception=True,  # if serializer is invalid raise exception and exit function
        )

        # get the user or None
        user = authenticate(
            request=request,
            username=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )

        if not user:
            #  if the user object is none, raise exception
            raise AuthenticationFailed(
                detail="no active account found with the given credentials",
                code="no_acive_account",
                # or {}
            )
        try:
            refresh = RefreshToken.for_user(user)
        except TokenError:
            raise exceptions.BadRequest(
                detail="Invalid Token",
                code="invalid_token",
            )

        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )


class TokenRefreshView(jwt_views.TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh = RefreshToken(serializer.validated_data.get("refresh"))
        except TokenError:
            raise exceptions.BadRequest(
                {"detail": "Invalid Token", "code": "invalid_token"}
            )

        if jwt_settings.ROTATE_REFRESH_TOKENS:
            refresh.set_jti()
            refresh.set_exp()

        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status.HTTP_200_OK,
        )
