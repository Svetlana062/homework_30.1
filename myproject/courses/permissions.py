from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    """Разрешает доступ только пользователям из группы 'Модераторы'."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )


class IsOwnerOrReadOnly(BasePermission):
    """Разрешено редактировать только владельцу объекта, а для просматривать — всем."""

    def has_object_permission(self, request, view, obj):
        # чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True
        # редактирование — только владельцу
        return hasattr(obj, "owner") and obj.owner == request.user


class IsModeratorOrReadOnly(BasePermission):
    """Разрешает только модераторам редактировать объекты,
    а чтение — всем."""

    def has_permission(self, request, view):
        # Разрешить всем безопасные методы
        if request.method in SAFE_METHODS:
            return True
        # Для POST и DELETE — запрещено всем (в том числе модераторам)
        if request.method in ["POST", "DELETE"]:
            return False
        # Для остальных методов — проверка на модератора
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )

    def has_object_permission(self, request, view, obj):
        # Чтение — всем; изменение — только модераторам
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )
