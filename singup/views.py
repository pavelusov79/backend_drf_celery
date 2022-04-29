from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .serializers import UserSerializer


class UserSingUpApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    