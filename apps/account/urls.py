from django.urls import path

from . import views

urlpatterns = [
    # User Authentication Endpoints
    path(
        "auth/login/",
        views.AuthView.as_view({"post": "login"}),
        name="login",
    ),
    # Endpoint for user login. Accepts POST requests with user credentials (email and password).
    # Returns an authentication token upon successful login.
    path(
        "auth/email/register/",
        views.AuthView.as_view({"post": "register"}),
        name="register",
    ),
    # Endpoint for user registration. Accepts POST requests with user details (email, password, etc.).
    # Creates a new user and sends an email with an OTP for verification.
    path(
        "auth/email/confirm/",
        views.AuthView.as_view({"post": "confirm_email"}),
        name="confirm_email",
    ),
    # Endpoint for confirming user email with OTP. Accepts POST requests with email and OTP code.
    # Verifies email and activates the user account if OTP is correct.
    path(
        "auth/email/confirm/request/",
        views.AuthView.as_view({"post": "request_confirm_email"}),
        name="request_confirm_email",
    ),
    # Endpoint to resend the email confirmation OTP. Accepts POST requests with user email.
    # Sends a new OTP to the user if the email is not verified.
    # Password Reset Endpoints
    path(
        "reset-password/request/",
        views.ResetPasswordView.as_view({"post": "request_email"}),
        name="request_password_reset",
    ),
    # Endpoint to request a password reset. Accepts POST requests with user email.
    # Sends a password reset email with an OTP to the provided email address.
    path(
        "reset-password/confirm/",
        views.ResetPasswordView.as_view({"post": "confirm_email"}),
        name="confirm_password_reset",
    ),
    # Endpoint for confirming password reset with OTP. Accepts POST requests with email and OTP code.
    # Verifies the OTP before allowing the user to proceed with setting a new password.
    path(
        "reset-password/set-password/",
        views.ResetPasswordView.as_view({"post": "update_password"}),
        name="set_new_password",
    ),
    # Endpoint to set a new password after password reset confirmation. Accepts POST requests with email, OTP, and new password.
    # Updates the user's password if OTP verification is successful.
]
