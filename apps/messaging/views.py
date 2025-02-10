from collections import OrderedDict

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from .models import UserDevice, UserMessage
from .serializers import UserDeviceSerializer, UserMessageSerializer


def get_list_inapp_message_queryset(request):
    return UserMessage.objects.filter(user=request.user, send_in_app=True).order_by("-created_at")


class MessagetListPagination(PageNumberPagination):
    def get_unseen_count(self):
        qs = get_list_inapp_message_queryset(self.request)
        return qs.filter(is_seen=False).count()

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("unseen_count", self.get_unseen_count()),
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class UserMessageView(ModelViewSet):
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    pagination_class = MessagetListPagination

    def get_queryset(self):
        return get_list_inapp_message_queryset(self.request)

    @swagger_auto_schema(request_body=Serializer)
    def seen(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_seen = True
        obj.save()

        return Response({"is_seen": True})


class UserDeviceView(ModelViewSet):
    serializer_class = UserDeviceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "token"

    def create(self, request, *args, **kwargs):
        serializer: UserDeviceSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_token = serializer.validated_data.get("token")
        user = self.request.user
        t, _ = UserDevice.objects.get_or_create(user=user, token=device_token)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
