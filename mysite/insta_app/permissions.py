from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Владелец или админ может редактировать/удалять пост или комментарий.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'author', None) or getattr(obj, 'user', None)
        return owner == request.user
