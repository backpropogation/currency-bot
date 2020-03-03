from django.db import models


class Currency(models.Model):
    rate = models.ForeignKey(
        'currency.Rate',
        related_name='currencies',
        on_delete=models.CASCADE,
        verbose_name='Rate'
    )
    rate_to_base_currency = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Rate to base currency'
    )
    name = models.CharField(
        max_length=4,
        verbose_name='Currency code'
    )

    def __str__(self):
        return self.name
