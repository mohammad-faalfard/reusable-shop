from collections import OrderedDict
from typing import Any, Dict

from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import HttpResponseRedirect, render
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from core.admin import BaseModelAdmin

from .forms import AddToGroupForm
from .models import (
    Group,
    GroupMessage,
    GroupUser,
    UserDevice,
    UserMessage,
)


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    list_display = ("title",)


@admin.register(GroupUser)
class GroupUserAdmin(BaseModelAdmin):
    list_display = ("id", "group", "user")


@admin.register(UserDevice)
class UserDeviceAdmin(BaseModelAdmin):
    list_display = ("id", "token", "user")


@admin.register(GroupMessage)
class GroupMessageAdmin(BaseModelAdmin):
    list_display = (
        "group",
        "title",
        "send_in_app",
        "send_notification",
        "send_email",
        "send_sms",
    )


@admin.register(UserMessage)
class UserMessageAdmin(BaseModelAdmin):
    list_display = (
        "user",
        "title",
        "send_in_app",
        "send_notification",
        "send_email",
        "send_sms",
    )
    readonly_fields = ("event_type", "event_data")
    autocomplete_fields = ("user",)
    search_fields = ["user"]

    def changelist_view(self, request: HttpRequest, extra_context: Dict[str, str] | None = None) -> TemplateResponse:
        return super().changelist_view(request, extra_context)


class AddUserToGroupMixin:
    actions = []

    @admin.action(description=_("add user to group"))
    def add_user_to_group(self, request, queryset):
        if "apply" in request.POST:
            form = AddToGroupForm(request.POST)
            if form.is_valid():
                GroupUser.objects.filter(group=form.cleaned_data["group"], user__in=queryset).delete()
                group_users = []
                for user in queryset:
                    group_users.append(GroupUser(group=form.cleaned_data["group"], user=user))

                GroupUser.objects.bulk_create(group_users)

                msg = _("users successfuly added to group")
                messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        form = AddToGroupForm(initial={"_selected_action": queryset.values_list("id", flat=True)})

        context = {
            **self.admin_site.each_context(request),
            "form": form,
        }

        return render(request, "messaging/add_to_group.html", context=context)

    def get_actions(self, request: HttpRequest) -> OrderedDict[Any, Any]:
        self.actions.append("add_user_to_group")
        return super().get_actions(request)
