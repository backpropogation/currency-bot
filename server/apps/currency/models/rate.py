from django.db import models


class Rate(models.Model):
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Datetime of parsing'
    )
    base_currency = models.CharField(
        max_length=4,
        verbose_name='Base currency'
    )

    def __str__(self):
        return f"{self.date.strftime('Rate parsed on %d.%m.%Y at %H:%M:%S')}"

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
