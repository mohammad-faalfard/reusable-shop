from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..serializers import (
    LoginSerializer,
    RegisterConfirmSerializer,
    RegisterSerializer,
    ResetPasswordRequestSerializer,
    UserSerializer,
)
from ..utils import send_verify_email_mail

# Retrieve the custom user model for authentication.
User = get_user_model()


def get_or_create_token(user):
    """
    Retrieve or create a token for the authenticated user.
    :param user: User instance for whom the token is generated.
    :return: Token object for the user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class AuthView(ViewSet):
    """
    ViewSet for managing user authentication tasks, including:
      - Login
      - Registration
      - Email confirmation
      - Resending email verification
    Each endpoint is annotated with swagger documentation for API representation.
    """

    @swagger_auto_schema(request_body=LoginSerializer)
    def login(self, request, *args, **kwargs):
        """
        Handles user login by validating credentials and returning an auth token.
        :param request: HTTP request containing login data.
        :return: Response containing token and user data or an error message.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve user by email if they have verified their email.
        user = User.objects.filter(email=serializer.validated_data["email"], is_verified_email=True).last()

        # Check if user exists and if the password is correct.
        if user and user.check_password(serializer.validated_data["password"]):
            token = get_or_create_token(user)
            return Response({"token": f"Token {token.key}", "user": UserSerializer(user).data})

        # Return error if authentication fails.
        return Response(
            {"detail": "Authentication credential were not provided."},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    @swagger_auto_schema(request_body=RegisterSerializer)
    def register(self, request, *args, **kwargs):
        """
        Handles user registration, creates an unverified user, and sends a verification email.
        :param request: HTTP request containing registration data.
        :return: Response indicating success or error message.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).last()

        # If user exists and is verified, return an error.
        if user and user.is_verified_email:
            return Response(
                {"detail": "Email already exists."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        # Delete unverified user to prevent duplicate email entries.
        elif user and not user.is_verified_email:
            user.delete()

        # Prepare data for new user registration.
        data = {**serializer.validated_data, "is_verified_email": False}
        data["username"] = serializer.validated_data["email"]

        # Create a new user, set password, and save user to the database.
        user = User.objects.create(**data)
        user.set_password(data["password"])
        user.save()

        # Generate an OTP for email verification and send verification email.
        otp = user.set_otp()
        send_verify_email_mail(
            request=request,
            email=user.email,
            code=otp,
            name=user.full_name,
        )

        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=RegisterConfirmSerializer)
    def confirm_email(self, request, *args, **kwargs):
        """
        Confirms the user's email using the provided OTP and grants an auth token.
        :param request: HTTP request containing email confirmation data.
        :return: Response containing token and user data or an error message.
        """
        serializer = RegisterConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        user = User.objects.filter(email=email).last()

        # Check OTP validity and mark email as verified if successful.
        if user and user.check_otp(code):
            user.verify_email()
            token = get_or_create_token(user)
            return Response({"token": f"Token {token.key}", "user": UserSerializer(user).data})

        # Return error if OTP verification fails.
        return Response(
            {"detail": "Authentication credential were not provided."},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    @swagger_auto_schema(request_body=ResetPasswordRequestSerializer)
    def request_confirm_email(self, request, *args, **kwargs):
        """
        Resends email verification OTP if the user's email is not verified.
        :param request: HTTP request containing email data.
        :return: Response indicating success or an error message.
        """
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).last()

        # Send new OTP if the user email is not verified.
        if user and not user.is_verified_email:
            otp = user.set_otp()
            send_verify_email_mail(
                request=request,
                email=user.email,
                code=otp,
                name=user.full_name,
            )
            return Response({"status": "ok"})

        # Return error if user is verified or does not exist.
        return Response(
            {"detail": "Authentication credential were not provided."},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
