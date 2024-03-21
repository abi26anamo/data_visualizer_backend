from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


# Retrieve the custom user model specified in the settings
User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """
    Serializer for creating a new user instance.
    Inherits from djoser's UserCreateSerializer.
    """
    class Meta(UserCreateSerializer.Meta):
        """
        Meta class defining the model and fields for the serializer.
        """
        model = User  # Sets the model to the custom user model retrieved by get_user_model()
        fields = ("id", "email", "name", "password")  # Specifies the fields to include in the serializer
