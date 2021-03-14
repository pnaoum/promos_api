from rest_framework.permissions import BasePermission

from apps.users.constants import ADMIN_USER


class IsAdmin(BasePermission):
    """
    Allow POST operation only if the user is a buyer
    """

    def has_permission(self, request, view):
        return request.user.role == ADMIN_USER
