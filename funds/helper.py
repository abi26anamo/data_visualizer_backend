from django.db.models import Sum

from .models import (
    FundCategory,
    DailyFundAllocationsModel,
    DailyFundCategoryAllocationsModel,
)


def get_queryset(category_id):
    """
    Retrieves the queryset of fund flows and related information for a given category.

    Args:
        category_id (int): The ID of the category.

    Returns:
        dict: A dictionary containing the fund flows data and the category name.
            Example:
            {
                "data": [
                    {
                        "date": "2022-01-01",
                        "aum_sum": 1000000,
                        "value": 500000
                    },
                    ...
                ],
                "category": "Category Name"
            }
    """
    response = {"data": [], "category": ""}
    if category := FundCategory.objects.filter(pk=category_id).first():
        response = {
            "data": list(
                category.get_fund_flows()
                .values("date")
                .annotate(aum_sum=Sum("aum"), value=Sum("category_flow"))
                .order_by("date")
            ),
            "category": category.name,
        }
    return response


def get_fund_categories_queryset():
    """
    Get queryset of all fund categories ordered by ID.

    :return: QuerySet of FundCategory objects.
    """
    return FundCategory.objects.all().order_by("id")


def get_daily_fund_category_allocations_queryset():
    """
    Get queryset of all daily fund category allocations ordered by ID.

    :return: QuerySet of DailyFundCategoryAllocationsModel objects.
    """

    return DailyFundCategoryAllocationsModel.objects.all().order_by("id")


def get_daily_fund_allocations_queryset():
    """
    Get queryset of all daily fund allocations ordered by ID.

    :return: QuerySet of DailyFundAllocationsModel objects.
    """
    return DailyFundAllocationsModel.objects.all().order_by("id")
