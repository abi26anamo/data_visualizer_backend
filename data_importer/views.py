from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TimeValuePair, UserUploadedData
from .serializers import UserUploadedDataSerializer, UserUploadedCategorySerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class UploadDataView(APIView):
    """
    API view to handle uploading user data and associated time-value pairs.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Get method to retrieve all user uploaded data.
        """
        user_uploaded_data = UserUploadedData.objects.all()
        serializer = UserUploadedDataSerializer(user_uploaded_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Post method to upload user data and associated time-value pairs.
        """
        serializer = UserUploadedDataSerializer(data=request.data)
        if serializer.is_valid():
            # Save UserUploadedData instance
            user_uploaded_data_instance = serializer.save()

            # Process and save time-value pairs
            time_value_pairs_data = request.data.get("data", [])
            current_time_zone = timezone.get_current_timezone()
            for pair_data in time_value_pairs_data:
                TimeValuePair.objects.create(
                    user_uploaded_data=user_uploaded_data_instance,
                    timestamp=timezone.datetime.fromtimestamp(
                        int(pair_data[0]) / 1000, current_time_zone
                    ),
                    value=pair_data[1],  # Value is the second element
                )

            # Retrieve updated serializer data with populated time_value_pairs
            updated_serializer = UserUploadedDataSerializer(user_uploaded_data_instance)
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDataDetailView(APIView):
    """
    API view to retrieve specific user uploaded data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        """
        Get method to retrieve user uploaded data by id.
        """
        try:
            user_uploaded_data = UserUploadedData.objects.get(id=id)
            serializer = UserUploadedDataSerializer(user_uploaded_data)
            return Response(serializer.data)
        except UserUploadedData.DoesNotExist:
            return Response(
                {"error": "User uploaded data with id {} does not exist".format(id)},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserUploadedCategoriesAPIView(APIView):
    """
    API view to retrieve user uploaded categories.
    This view is used to retrieves the user uploaded categories queryset, serializes it using UserUploadedCategorySerializer,
    and returns the serialized data along with the count of categories.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get method to retrieve user uploaded categories.
        """
        # Get user uploaded categories
        user_categories = UserUploadedData.objects.all()
        serializer = UserUploadedCategorySerializer(user_categories, many=True).data

        return Response({"results": serializer, "count": len(serializer)})
