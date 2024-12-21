from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from core_apps.profiles.models import Profile

from .serializers import UserSerializer


class CustomUserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        # Check if the user has a profile, and create one if not
        if not hasattr(user, "profile"):
            Profile.objects.create(user=user)
        return user

    def get_queryset(self):
        return get_user_model().objects.none()
