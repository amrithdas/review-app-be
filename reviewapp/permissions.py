from rest_framework.permissions import IsAuthenticated

class IsAuthenticatedOrReadOnlyForSwagger(IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return request.method in ['GET', 'HEAD', 'OPTIONS']
