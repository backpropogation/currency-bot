from django.conf import settings
from django.core.cache import cache

from apps.currency.models import Rate


def get_currencies_of_latest_rate():
    currencies_names = cache.get(
        settings.LATEST_RATE_CURRENCIES,
        list(Rate.objects.last().currencies.values_list('name', flat=True))
    )
    return currencies_names
