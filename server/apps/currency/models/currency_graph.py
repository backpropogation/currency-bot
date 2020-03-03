from django.db import models


class CurrencyGraph(models.Model):
    currency_name = models.CharField(max_length=4)
    image = models.ImageField(upload_to='graphs')

    def __str__(self):
        return f'{self.currency_name} graph'

    class Meta:
        verbose_name = 'Currency graph'
        verbose_name_plural = 'Currency graphs'
