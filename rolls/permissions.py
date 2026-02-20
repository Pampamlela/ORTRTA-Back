from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permission qui vérifie que l'objet appartient à l'utilisateur connecté.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsRollOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.roll.user == request.user