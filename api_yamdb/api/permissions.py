from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.role == 'admin'
                    or request.user.is_superuser)
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешаем любые действия с объектом только автору объекта.
    Анонимам разрешено только чтение или работа с безопасными
    методам (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if request.method == 'POST':
                return True
            return (request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user)
