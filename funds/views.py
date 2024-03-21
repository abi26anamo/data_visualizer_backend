from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .helper import (
    get_fund_categories_queryset,
    get_queryset,
    get_daily_fund_allocations_queryset,
    get_daily_fund_category_allocations_queryset,
)
from .serializers import (
    FundCategorySerializer,
    FundFlowSerializer,
    DailyFundAllocationsSerializer,
    DailyFundCategoryAllocationsSerializer,
)


class DailyFundFlowSeriesAPIView(APIView):
    """
    API view for retrieving daily fund flow series.

    This view accepts a category_id parameter in the request query parameters
    and returns the fund flow series data for the specified category.

    Example usage:
    GET /api/fund-flow-series/?category_id=1

    Parameters:
    - category_id (int): The ID of the category for which to retrieve the fund flow series.

    Returns:
    A JSON response containing the fund flow series data for the specified category.
    The response has the following structure:
    {
        "results": [
            {
                "name": "Category Name",
                "data": [data points]
            }
        ]
    }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serie_obj = []
        if category_id := request.GET.get("category_id", None):
            category_data = get_queryset(category_id)
            serie_obj = [
                {"name": category_data["category"], "data": category_data["data"]}
            ]

        serializer = FundFlowSerializer(serie_obj, many=True).data

        return Response({"results": serializer})


class FundCategoriesAPIView(APIView):
    """
    API view for retrieving fund categories.

    Methods:
    - get: Retrieves the fund categories queryset, serializes it using FundCategorySerializer,
           and returns the serialized data along with the count of categories.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        categories = get_fund_categories_queryset()
        serializer = FundCategorySerializer(categories, many=True).data
        return Response({"results": serializer, "count": len(serializer)})


class DailyFundAllocationsAPIView(APIView):
    """
    API view for retrieving daily fund allocations.

    Methods:
    - get: Retrieves the daily fund allocations queryset, serializes it using DailyFundAllocationsSerializer,
           and returns the serialized data along with the count of allocations.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        allocations = get_daily_fund_allocations_queryset()
        serializer = DailyFundAllocationsSerializer(allocations, many=True).data
        return Response({"results": serializer, "count": len(serializer)})


class DailyFundCategoryAllocationsAPIView(APIView):
    """
    API view for retrieving daily fund category allocations.

    Methods:
    - get: Retrieves the daily fund category allocations queryset, serializes it using DailyFundCategoryAllocationsSerializer,
           and returns the serialized data along with the count of allocations.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        allocations = get_daily_fund_category_allocations_queryset()
        serializer = DailyFundCategoryAllocationsSerializer(allocations, many=True).data
        return Response({"results": serializer, "count": len(serializer)})
