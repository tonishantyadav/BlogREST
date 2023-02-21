from rest_framework import permissions

class IsAdminOrAuthor(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.author or request.user.is_staff
