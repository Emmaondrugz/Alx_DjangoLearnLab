from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'actor', 'actor_username', 'verb',
            'target_type', 'target_object_id', 'is_read', 'timestamp'
        )
        read_only_fields = ('id', 'actor', 'timestamp', 'target_type')

    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model  # returns 'post', 'comment', etc.
        return None
