from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_obj_permission(self, request, view, obj):
        return obj.controller == request.user