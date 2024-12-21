from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender", required=False)
    phone_number = PhoneNumberField(source="profile.phone_number", required=False)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(source="profile.country", required=False)
    city = serializers.CharField(source="profile.city", required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "profile_photo",
            "country",
            "city",
        ]

    def get_profile_photo(self, instance):
        # Safeguard profile and photo access
        if instance.profile and instance.profile.profile_photo:
            return instance.profile.profile_photo.url
        return None

    def to_representation(self, instance):
        if not hasattr(instance, "profile"):
            return {  # Return Default values if no profile exist
                "id": instance.id,
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "gender": None,
                "phone_number": None,
                "profile_photo": None,
                "country": None,
                "city": None,
            }
        return super().to_representation(instance)  # If the user does have a profile


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password1": self.validated_data.get("password1", ""),
        }

    def save(self, request):
        adaptor = get_adapter()  # returns the adaptor class which is currently active
        user = adaptor.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adaptor.save_user(request, user, self)
        user.save()

        setup_user_email(request, user, [])
        user.email = self.cleaned_data.get("email")
        user.password = self.cleaned_data.get("password1")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")

        return user
