from rest_framework import serializers


class CustomListField(serializers.ListField):
    """
    A custom list field serializer that converts data into a list of lists.

    This serializer is specifically designed to handle data that represents points
    with a "date" and "value" field. It converts the data into a list of lists,
    where each inner list contains the "date" and "value" as its elements.
    """

    def to_representation(self, data):
        return [[point["date"], float(point["value"])] for point in data]


class FundCategorySerializer(serializers.Serializer):
    """
    Serializer for Fund Category model.
    """

    id = serializers.IntegerField()
    name = serializers.CharField()


class FundFlowSerializer(serializers.Serializer):
    """
    Serializer for FundFlow model.
    """

    name = serializers.CharField()
    data = CustomListField()


class DailyFundAllocationsSerializer(serializers.Serializer):
    """
    Serializer for Fund Category model.
    """

    date = serializers.DateField()
    allocation = serializers.FloatField()
    benchmark = serializers.IntegerField()
    category = FundCategorySerializer()
    factsheet_count = serializers.IntegerField()
    difference = serializers.FloatField()
    aum_sum = serializers.FloatField()
    aum_wieghted_average_allocation = serializers.FloatField()


class DailyFundCategoryAllocationsSerializer(serializers.Serializer):
    """
    Serializer for Fund DailyFundCategoryAllocationsModel model.
    """

    date = serializers.DateField()
    category = FundCategorySerializer()
    allocation = serializers.FloatField()
    benchmark = serializers.IntegerField()
