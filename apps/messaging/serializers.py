from rest_framework import serializers

from .models import UserMessage


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "is_seen",
            "event_type",
            "event_data",
        )
        read_only_fields = fields


class UserDeviceSerializer(serializers.Serializer):
    token = serializers.UUIDField()
