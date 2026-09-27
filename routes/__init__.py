# Routes package

from .auth import auth_bp
from .bikes import bikes_bp
from .booking import booking_bp
from .admin import admin_bp

__all__ = [
    "auth_bp",
    "bikes_bp",
    "booking_bp",
    "admin_bp"
]