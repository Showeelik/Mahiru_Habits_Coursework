from rest_framework.permissions import BasePermission

class IsOwnerOrPublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.user == request.user
