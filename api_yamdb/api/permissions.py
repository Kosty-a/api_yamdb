from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    '''Разрешаем добавление, обновление или удаление объектов администратору.
    Остальным пользователям разрешено только чтение или работа с безопасными
    методам (GET, HEAD, OPTIONS).
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.role == 'admin'
                    or request.user.is_superuser)
        return False


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    '''Разрешаем добавление объектов аутентифицированным пользователям.
    Обновление или удаление объектов разрешаем автору объекта,
    модератору или администратору. Остальным пользователям разрешено
    только чтение или работа с безопасными методам (GET, HEAD, OPTIONS).
    '''

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
