from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # SAFE METHODS: 'GET', 'HEAD', 'OPTIONS'
            return True
        
        return obj.author == request.user # check the object's author is matched with logged in user