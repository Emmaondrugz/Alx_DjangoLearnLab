from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # check request method that was made
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            # return true is req method is anything
            # other than the above
            return True

        # checks if the request user is the author
        return obj.author == request.user
