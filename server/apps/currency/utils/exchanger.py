from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.cache import cache


class Exchanger:
    @staticmethod
    def exchange(from_currency, to_currency, amount):
        latest_rate = cache.get(settings.LATEST_EXCHANGE_RATES)
        from_currency_rate = latest_rate.get(from_currency)
        to_currency_rate = latest_rate.get(to_currency)
        exchange = Decimal(float(amount)) / from_currency_rate * to_currency_rate
        return {
            'result': str(exchange.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)),
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'base_currency': latest_rate.get('base_currency')
        }
