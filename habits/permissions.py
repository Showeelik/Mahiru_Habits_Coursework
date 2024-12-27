from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ только владельцу объекта для изменения,
    но разрешает чтение всем.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем только безопасные методы (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return obj.is_public or obj.user == request.user
        # Разрешаем изменения только владельцу объекта
        return obj.user == request.user
