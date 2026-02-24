from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list and retrieve for notifications.
    Standard list returns all; use ?unread=true to filter.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user).order_by('-timestamp')

        # Implementation of "showcasing unread notifications"
        unread_only = self.request.query_params.get('unread')
        if unread_only == 'true':
            queryset = queryset.filter(is_read=False)
        return queryset

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marks a single notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Marks all notifications for the user as read"""
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all notifications marked as read'}, status=status.HTTP_200_OK)