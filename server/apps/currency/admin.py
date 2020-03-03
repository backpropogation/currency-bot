from django.contrib import admin
from apps.currency.models import Currency, Rate, CurrencyGraph


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.register(CurrencyGraph)
class CurrencyGraphAdmin(admin.ModelAdmin):
    pass
