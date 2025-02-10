from datetime import timedelta
from typing import Any

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from unfold.decorators import action
from unfold.forms import AdminPasswordChangeForm

from apps.messaging.admin import AddUserToGroupMixin
from core.admin import BaseModelAdmin

from .forms import AdminUserCreationForm, NormalUserCreationForm
from .models import Address, AdminUserProxy, NewUserProxy, NormalUserProxy, User


@admin.register(AdminUserProxy)
class AdminUserAdmin(AddUserToGroupMixin, BaseModelAdmin, DjangoUserAdmin):
    add_form = AdminUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("id", "phone_number", "username", "email", "first_name", "last_name", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone_number", "username", "first_name", "last_name", "email")

    add_form_template = "admin/auth/user/add_form.html"
    fieldsets = (
        (
            _("General"),
            {
                "classes": ["tab"],
                "fields": (
                    "phone_number",
                    "username",
                ),
            },
        ),
        (_("Personal Info"), {"classes": ["tab"], "fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {"classes": ["tab"], "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"classes": ["tab"], "fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "phone_number", "username", "password1", "password2"),
            },
        ),
    )
    ordering = ("id",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter((Q(is_staff=True) | Q(is_superuser=True)))


@admin.register(NormalUserProxy)
class NormalUserProxyAdmin(AddUserToGroupMixin, BaseModelAdmin, DjangoUserAdmin):
    add_form = NormalUserCreationForm
    list_display = ("id", "phone_number", "username", "first_name", "last_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("phone_number", "username", "first_name", "last_name", "email")

    add_form_template = "admin/auth/user/add_form.html"
    fieldsets = (
        (_("general"), {"classes": ["tab"], "fields": ("first_name", "last_name")}),
        (
            _("Contact Info"),
            {
                "classes": ["tab"],
                "fields": (
                    "phone_number",
                    "username",
                    "email",
                ),
            },
        ),
        (_("Important dates"), {"classes": ["tab"], "fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    ordering = ("id",)
    actions_detail = ["open_wallet", "change_detail_action_unblock", "change_detail_action_block"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False).exclude(is_superuser=True)

    @action(description=_("wallet"), url_path="wallet")
    def open_wallet(self, request: HttpRequest, object_id: int):
        user = User.objects.get(pk=object_id)

        return redirect(reverse_lazy("admin:wallet_wallet_change", args=(user.wallet_id,)))

    @action(description=_("block & deactivate"), url_path="block", attrs={"style": "background-color: #ff7675;color:white;"})
    def change_detail_action_block(self, request: HttpRequest, object_id: int):
        messages.info(request, _("user blocked"))
        User.objects.filter(pk=object_id).update(is_active=False)
        return redirect(reverse_lazy("admin:account_customeruserproxy_change", args=(object_id,)))

    @action(description=_("unblock & activate"), url_path="unblock", attrs={"style": "background-color: #00cec9;color:white;"})
    def change_detail_action_unblock(self, request: HttpRequest, object_id: int):
        messages.success(request, _("user unblocked"))

        User.objects.filter(pk=object_id).update(is_active=True)
        return redirect(reverse_lazy("admin:account_customeruserproxy_change", args=(object_id,)))

    def get_actions_detail(self, request, object_id: int = None):
        user = User.objects.get(id=object_id)
        actions = []

        for a in self._get_base_actions_detail():
            if user.is_active:
                if "change_detail_action_unblock" in a.action_name:
                    continue
            else:
                if "change_detail_action_block" in a.action_name:
                    continue

            actions.append(a)

        return self._filter_unfold_actions_by_permissions(request, actions)


@admin.register(NewUserProxy)
class NewUserProxyAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "username",
    )
    search_fields = ("phone_number", "username", "first_name", "last_name", "email")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        user = User.objects.get(id=object_id)
        if user.is_superuser or user.is_staff:
            return redirect(reverse_lazy("admin:account_adminuserproxy_change", args=(object_id,)))
        else:
            return redirect(reverse_lazy("admin:account_normaluserproxy_change", args=(object_id,)))

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        start_time = (timezone.now() - timedelta(days=1)).date()
        return NewUserProxy.objects.filter(date_joined__date__gte=start_time)


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    list_display = ("name",)


# registered only for autocomplete fields to work
@admin.register(User)
class UserAdmin(BaseModelAdmin):
    ordering = [
        "id",
    ]
    exclude = ("username",)
    search_fields = ("phone_number", "national_code")

    def change_view(
        self, request: HttpRequest, object_id: str, form_url: str = ..., extra_context: dict[str, bool] | None = ...
    ) -> HttpResponse:
        user = User.objects.get(pk=object_id)
        if user.is_staff or user.is_superuser:
            return redirect(reverse_lazy("admin:account_adminuserproxy_change", args=(object_id,)))
        return redirect(reverse_lazy("admin:account_normaluserproxy_change", args=(object_id,)))


class AddressAdmin(BaseModelAdmin):
    """
    Admin interface for managing Address instances.
    """

    list_display = (
        "id",
        "title",
        "user",
        "postal_code",
        "city",
        "street",
        "is_active",
    )
    list_filter = ("is_active", "user")
    search_fields = ("title", "user__username", "postal_code", "city", "street")
    ordering = ("-created_at",)
    fieldsets = ((None, {"fields": ("is_active", "title", "user", "city", "postal_code", "street")}),)


# Register the Address model with the custom admin interface
admin.site.register(Address, AddressAdmin)
