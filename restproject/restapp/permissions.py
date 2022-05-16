from rest_framework import permissions


class UserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return False
        return obj.owner == request.user
