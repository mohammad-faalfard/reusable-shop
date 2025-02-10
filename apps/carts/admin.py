from django.contrib import admin
from unfold.admin import StackedInline

from core.admin import BaseModelAdmin

from .models import Cart, CartItem


class CartItemInline(StackedInline):
    model = CartItem
    extra = 0
    tab = True


@admin.register(Cart)
class CartModelAdmin(BaseModelAdmin):
    list_display = ["user", "session_id", "created_at"]
    inlines = [CartItemInline]
