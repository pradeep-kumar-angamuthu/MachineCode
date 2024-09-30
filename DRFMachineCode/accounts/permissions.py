# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role + "IsSuperAdmin")
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}, Role: {getattr(request.user, 'role', None)}")
        return request.user.is_authenticated and request.user.role == 'SUPERADMIN'

class IsManager(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role +" IsManager")
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}, Role: {getattr(request.user, 'role', None)}")
        return request.user.is_authenticated and request.user.role == 'MANAGER' #'MANAGER'

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role+ " IsSupervisor")
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}, Role: {getattr(request.user, 'role', None)}")
        return request.user.is_authenticated and request.user.role == 'SUPERVISOR'

class IsOperator(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role + " IsOperator")
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}, Role: {getattr(request.user, 'role', None)}")
        return request.user.is_authenticated and request.user.role == 'OPERATOR'

class IsAnyRole(BasePermission):
    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.role == 'MANAGER') or
            (request.user.is_authenticated and request.user.role == 'SUPERVISOR') or
            (request.user.is_authenticated and request.user.role == 'OPERATOR') or
            (request.user.is_authenticated and request.user.role == 'SUPERADMIN')
        )