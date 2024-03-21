from rest_framework import serializers

# Importing necessary modules
from .models import TimeValuePair, UserUploadedData


# Serializer for TimeValuePair model
class TimeValuePairSerializer(serializers.ModelSerializer):
    """
    Serializer for TimeValuePair model.

    This serializer converts TimeValuePair objects into JSON representation,
    including the timestamp and value fields.
    """

    # Serializer method field for timestamp
    timestamp = serializers.SerializerMethodField()

    # Method to get timestamp
    def get_timestamp(self, obj: TimeValuePair):
        return obj.timestamp.timestamp()

    class Meta:
        model = TimeValuePair  # Using TimeValuePair model
        fields = ["timestamp", "value"]  # Fields to be included in the serialization


# Serializer for UserUploadedData model
class UserUploadedDataSerializer(serializers.ModelSerializer):
    """
    Serializer for UserUploadedData model.

    This serializer converts UserUploadedData objects into JSON representation,
    including the ID, name, and associated time-value pairs.
    """

    # Serializer for time-value pairs
    time_value_pairs = TimeValuePairSerializer(many=True, read_only=True)

    class Meta:
        model = UserUploadedData  # Using UserUploadedData model
        fields = ["id", "name", "time_value_pairs"]  # Defining fields to include in serialization


# Serializer for UserUploadedCategory
class UserUploadedCategorySerializer(serializers.Serializer):
    """
    Serializer for UserUploadedCategory.

    This serializer converts UserUploadedCategory objects into JSON representation,
    including the ID and name fields.
    """

    id = serializers.IntegerField()
    name = serializers.CharField()
