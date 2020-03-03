from django.conf import settings
from django.core.cache import cache
from django.test import TestCase

from apps.currency.models import Rate, CurrencyGraph, Currency
from apps.currency.serializers import RateSerializer, RateForExchangePurposeSerializer
from apps.currency.tasks import update_rates, draw_graphs
from config.celery import app


class CeleryTasksTestCase(TestCase):
    def setUp(self) -> None:
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.api_currencies_count = 33
        self.rates_count_after_migration = 1

    def test_update_rates_correctly_creates_models_and_sets_cache(self):
        update_rates.apply()
        self.assertEqual(Rate.objects.count(), 1)
        rate = Rate.objects.last()
        self.assertEqual(rate.currencies.count(), self.api_currencies_count)
        self.assertEqual(cache.get(settings.LATEST_RATE), RateSerializer(rate).data)
        self.assertEqual(cache.get(settings.LATEST_RATE_CURRENCIES),
                         list(rate.currencies.values_list('name', flat=True)))
        self.assertEqual(cache.get(settings.LATEST_EXCHANGE_RATES), RateForExchangePurposeSerializer(rate).data)

    def test_draw_graphs_correctly_create_models(self):
        rate = Rate.objects.create(base_currency='USD')
        Currency.objects.create(name='RUB', rate_to_base_currency=66.66, rate=rate)
        Currency.objects.create(name='EUR', rate_to_base_currency=0.91, rate=rate)
        draw_graphs.apply()
        self.assertEqual(CurrencyGraph.objects.count(), 2)
