from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..serializers import (
    ResetPasswordConfirmSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSetPasswordSerializer,
)
from ..utils import send_forget_password_mail

User = get_user_model()


class ResetPasswordView(ModelViewSet):
    """
    ViewSet for handling password reset functionality including
    sending reset email, confirming OTP, and updating the password.
    """

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=ResetPasswordRequestSerializer)
    def request_email(self, request, *args, **kwargs):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data["email"]).last()
        if user:
            otp = user.set_otp()
            send_forget_password_mail(
                request=request,
                email=user.email,
                code=otp,
                name=user.full_name,
            )

        return Response({"status": "ok"})

    @swagger_auto_schema(request_body=ResetPasswordConfirmSerializer)
    def confirm_email(self, request, *args, **kwargs):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).last()

        if user and user.check_otp(serializer.validated_data["code"]):
            token = user.set_reset_password_token()
            return Response({"reset_token": token})

        return Response(
            {"detail": "Authentication credential were not provided."},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    @swagger_auto_schema(request_body=ResetPasswordSetPasswordSerializer)
    def update_password(self, request, *args, **kwargs):
        serializer = ResetPasswordSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(reset_password_token=serializer.validated_data["token"]).last()

        if user:
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"status": "ok"})

        return Response(
            {"detail": "Authentication credential were not provided."},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
