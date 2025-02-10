# apps/account/models/__init__.py

from .address import Address
from .otp_mixin import OTPMixin
from .proxy_models import AdminUserProxy, NewUserProxy, NormalUserProxy
from .user import User

__all__ = [
    "User",
    "OTPMixin",
    "AdminUserProxy",
    "NormalUserProxy",
    "NewUserProxy",
    "Address",
]
