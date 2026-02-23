from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Check if the user is in the 'Moderator' group.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderator').exists()

class IsOwner(permissions.BasePermission):
    """
    Check if the user is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
