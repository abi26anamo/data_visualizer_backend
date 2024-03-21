# Importing necessary modules
from django.db import models


# Definition of UserUploadedData model
class UserUploadedData(models.Model):
    """
    Model to represent user uploaded data.

    Attributes:
    - name: Name of the user uploaded data.
    """
    name = models.CharField(max_length=255, default="")  # Name of the user uploaded data

    def __str__(self):
        """
        String representation of the model.
        """
        return self.name

    class Meta:
        """
        Meta class for the model.

        Attributes:
        - db_table: Custom database table name.
        - verbose_name_plural: Plural name for the model in admin interface.
        """
        db_table = "user_uploaded_data"  # Custom database table name
        verbose_name_plural = "User uploaded data"  # Plural name for the model in admin interface


# Definition of TimeValuePair model
class TimeValuePair(models.Model):
    """
    Model to represent time-value pairs associated with user uploaded data.

    Attributes:
    - user_uploaded_data: ForeignKey relationship with UserUploadedData model.
    - timestamp: Timestamp associated with the value.
    - value: Numeric value associated with the timestamp.
    """
    user_uploaded_data = models.ForeignKey(
        UserUploadedData, related_name="time_value_pairs", on_delete=models.CASCADE
    )  # ForeignKey relationship with UserUploadedData model
    timestamp = models.DateTimeField()  # Timestamp associated with the value
    value = models.FloatField()  # Numeric value associated with the timestamp

    class Meta:
        """
        Meta class for the model.

        Attributes:
        - db_table: Custom database table name.
        """
        db_table = "time_value_pair"  # Custom database table name
