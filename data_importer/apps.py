from django.apps import AppConfig


class DataImporterConfig(AppConfig):
    """
    Configuration class for the Data Importer app.

    This class defines the configuration for the Data Importer app, including the default auto field
    and the app name.
    """

    default_auto_field = "django.db.models.BigAutoField"  # Setting the default auto field for models
    name = "data_importer"  # Setting the name of the app
