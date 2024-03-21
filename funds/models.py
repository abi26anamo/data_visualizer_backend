from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import SET_NULL, CharField, ForeignKey, Model, Q
from ordered_model.models import OrderedModel, OrderedModelQuerySet


class CategoryFundFlowDailyPlotseriesModel(Model):
    """
    Model representing daily plot series for fund flow categories.

    Attributes:
    - date: Date of the data.
    - category_id: ID of the category.
    - aum: Assets under management.
    - category_flow: Category flow.
    """
    date = models.DateField()
    category_id = models.IntegerField()
    aum = models.DecimalField(max_digits=15, decimal_places=6)
    category_flow = models.DecimalField(max_digits=15, decimal_places=6)

    class Meta:
        managed = True
        db_table = "plotseries_fundflow_category_daily"


class FundCategoryQuerySet(OrderedModelQuerySet):
    """
    QuerySet for FundCategory model with custom methods.
    """
    def get_category_flows_queryset(self):
        return CategoryFundFlowDailyPlotseriesModel.objects.filter(
            category_id__in=self.values_list("pk", flat=True),
            date__week_day__in=range(2, 7),
        )


class FundCategory(OrderedModel):
    """
    Model representing fund categories.

    Attributes:
    - name: Name of the category.
    - title: Title of the category.
    - parent: Parent category (if any).
    """

    name = CharField(max_length=255, unique=True, validators=[MinLengthValidator(1)])
    title = CharField(max_length=255, validators=[MinLengthValidator(1)])
    parent = ForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=SET_NULL
    )
    objects = FundCategoryQuerySet.as_manager()

    def get_fund_flows(self):
        return FundCategory.objects.get_category_flows_queryset().filter(
            Q(category_id=self.pk) | Q(category_id__in=self.children.all())
        )


class DailyFundAllocationsModel(Model):
    """
    Model representing daily fund allocations.

    Attributes:
    - date: Date of the data.
    - allocation: Allocation value.
    - benchmark: Benchmark value.
    - category: ForeignKey to FundCategory model.
    - factsheet_count: Factsheet count.
    - difference: Difference value.
    - aum_sum: Sum of assets under management.
    - aum_wieghted_average_allocation: Weighted average allocation value.
    """
    date = models.DateField()
    allocation = models.FloatField()
    benchmark = models.IntegerField()
    category = ForeignKey(FundCategory, on_delete=models.CASCADE)
    factsheet_count = models.IntegerField()
    difference = models.FloatField()
    aum_sum = models.FloatField()
    aum_wieghted_average_allocation = models.FloatField()

    class Meta:
        managed = True
        db_table = "daily_fund_allocations"


class DailyFundCategoryAllocationsModel(Model):
    """
    Model representing daily fund category allocations.

    Attributes:
    - date: Date of the data.
    - category: ForeignKey to FundCategory model.
    - allocation: Allocation value.
    - benchmark: Benchmark value.
    """
    date = models.DateField()
    category = ForeignKey(FundCategory, on_delete=models.CASCADE)
    allocation = models.FloatField()
    benchmark = models.IntegerField()

    class Meta:
        managed = True
        db_table = "daily_fund_category_allocations"
