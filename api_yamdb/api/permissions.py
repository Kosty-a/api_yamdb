from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    '''Разрешаем добавление, обновление или удаление объектов администратору.

    Остальным пользователям разрешено только чтение или работа с безопасными
    методам (GET, HEAD, OPTIONS).
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin
            )
        )


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    '''Разрешаем добавление объектов аутентифицированным пользователям.

    Обновление или удаление объектов разрешаем автору объекта,
    модератору или администратору. Остальным пользователям разрешено
    только чтение или работа с безопасными методам (GET, HEAD, OPTIONS).
    '''

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.method == 'POST')
            or request.user.is_admin or request.user.is_moderator
            or obj.author == request.user
        )
