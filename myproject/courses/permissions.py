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
    """Разрешено редактировать только владельцу объекта, а просматривать — всем."""

    def has_object_permission(self, request, view, obj):
        # чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True
        # редактирование — только владельцу
        return hasattr(obj, "owner") and obj.owner == request.user


class IsModeratorOrReadOnly(BasePermission):
    """Модераторы могут читать и редактировать, но не создавать и не удалять.
    Остальные — только читать."""

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
        # Всем разрешены безопасные методы
        if request.method in SAFE_METHODS:
            return True
        # Модераторы могут редактировать (PUT/PATCH)
        if request.method in ["PUT", "PATCH"]:
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.groups.filter(name="Модераторы").exists()
            )
        # Запретить удаление (DELETE)
        if request.method == "DELETE":
            return False
        # По умолчанию — запрещено
        return False
