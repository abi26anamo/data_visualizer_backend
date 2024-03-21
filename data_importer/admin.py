from django.contrib import admin
from .models import UserUploadedData, TimeValuePair
from django_admin_listfilter_dropdown.filters import DropdownFilter
from rangefilter.filters import DateRangeFilterBuilder

# Customizing admin site headers and titles
admin.site.site_header = "EXANTE DATA ADMIN"
admin.site.site_title = "EXANTE DATA"
admin.site.index_title = "Manage exante data"


class UserUploadedDataAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserUploadedData model.

    Attributes:
    - list_display: Fields to display in the list view.
    - list_per_page: Number of items to display per page in the list view.
    - search_fields: Fields to enable searching in the list view.
    - list_filter: Filters to be displayed in the list view with dropdown.
    - ordering: Default ordering for the list view.
    """

    list_display = ("name",)
    list_per_page = 10
    search_fields = ("name",)
    list_filter = [("name", DropdownFilter)]
    ordering = ("name",)


class TimeValuePairAdmin(admin.ModelAdmin):
    """
    Admin configuration for TimeValuePair model.

    Attributes:
    - list_display: Fields to display in the list view.
    - list_filter: Filters to be displayed in the list view with dropdown or date range.
    - list_per_page: Number of items to display per page in the list view.
    - get_user_uploaded_data: Custom method to display associated UserUploadedData name.
    - get_timestamp: Custom method to format timestamp.
    """

    list_display = ("get_user_uploaded_data", "get_timestamp", "value")
    list_filter = (
        ("user_uploaded_data__name", DropdownFilter),
        (
            "timestamp",
            DateRangeFilterBuilder(
                title="Filter by date",
            ),
        ),
    )
    list_per_page = 10  # Number of items per page

    def get_user_uploaded_data(self, obj):
        """
        Custom method to display associated UserUploadedData name.

        Returns:
        - Name of the UserUploadedData associated with the TimeValuePair.
        """
        return obj.user_uploaded_data.name

    def get_timestamp(self, obj):
        """
        Custom method to format timestamp.

        Returns:
        - Timestamp of the TimeValuePair formatted as "YYYY-MM-DD".
        """
        return obj.timestamp.strftime("%Y-%m-%d")


# Registering admin configurations for models
admin.site.register(UserUploadedData, UserUploadedDataAdmin)
admin.site.register(TimeValuePair, TimeValuePairAdmin)
