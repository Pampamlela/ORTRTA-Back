from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Autorise l'accès uniquement si l'objet appartient à l'utilisateur connecté.
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", None) == request.user # getattr évite une erreur si un modèle change
    
class IsRollOwner(BasePermission):
    """
    Autorise l'accès uniquement si la roll liée appartient à l'utilisateur connecté.
    """
    def has_object_permission(self, request, view, obj):
        roll = getattr(obj, "roll", None)
        return roll and roll.user == request.user