from django.db import models


class Currency(models.Model):
    rate = models.ForeignKey(
        'currency.Rate',
        related_name='currencies',
        on_delete=models.CASCADE
    )
    rate_to_base_currency = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    name = models.CharField(
        max_length=4
    )

    def __str__(self):
        return self.name
