from django.db import models


class Rate(models.Model):
    date = models.DateTimeField(
        auto_now_add=True
    )
    base_currency = models.CharField(
        max_length=4
    )

    def __str__(self):
        return f"{self.date.strftime('Rate parsed on %d.%m.%Y at %H:%M:%S')}"
