from django.urls import path

from .views import (
    DailyFundFlowSeriesAPIView,
    FundCategoriesAPIView,
    DailyFundAllocationsAPIView,
    DailyFundCategoryAllocationsAPIView,
)

urlpatterns = [
    path(
        "daily-fund-flow-series/",
        DailyFundFlowSeriesAPIView.as_view(),
        name="daily-fund-flow-series",
    ),
    path("fund-categories/", FundCategoriesAPIView.as_view(), name="fund-categories"),
    path(
        "daily-fund-allocations/",
        DailyFundAllocationsAPIView.as_view(),
        name="daily-fund-allocations",
    ),
    path(
        "daily-fund-category-allocations/",
        DailyFundCategoryAllocationsAPIView.as_view(),
        name="daily-fund-category-allocations",
    ),
]
