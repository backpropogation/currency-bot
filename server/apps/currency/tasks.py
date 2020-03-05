import datetime
import json
from uuid import uuid4

import matplotlib.pyplot as plt
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now

from apps.currency.models import Rate, Currency, CurrencyGraph
from apps.currency.serializers import RateSerializer, RateForExchangePurposeSerializer
from config.celery import app


@app.task(autoretry_for=(requests.exceptions.ConnectionError,), retry_kwargs={'max_retries': 5})
def update_rates():
    response = requests.get(settings.RATES_URL).json()
    if response:
        rate = Rate.objects.create(base_currency=response['base'])
        currencies = [
            Currency(name=currency, rate=rate, rate_to_base_currency=rate_to_base_currency)
            for currency, rate_to_base_currency in response['rates'].items()
        ]
        Currency.objects.bulk_create(currencies)
        cache.set(settings.LATEST_RATE, RateSerializer(rate).data, timeout=settings.RATE_TIMEOUT)
        cache.set(
            settings.LATEST_RATE_CURRENCIES,
            list(rate.currencies.values_list('name', flat=True)),
            timeout=settings.RATE_TIMEOUT
        )
        cache.set(
            settings.LATEST_EXCHANGE_RATES,
            RateForExchangePurposeSerializer(rate).data,
            timeout=settings.RATE_TIMEOUT
        )


@app.task(autoretry_for=(requests.exceptions.ConnectionError,), retry_kwargs={'max_retries': 5})
def draw_graphs():
    end_at = now()
    start_at = (end_at - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_at = end_at.strftime("%Y-%m-%d")

    for currency in Currency.objects.distinct('name'):
        currency_name = currency.name
        r = requests.get(
            f'https://api.exchangeratesapi.io/history?start_at={start_at}&end_at={end_at}&base=USD&symbols={currency_name}',
        )
        data = json.loads(r.text)
        rates_for_period = data.get('rates', None)
        if rates_for_period:
            dates = sorted(list(rates_for_period.keys()))
            rates = [data['rates'][date][currency_name] for date in dates]
            plt.plot_date(dates, rates, linestyle='solid')
            plt.title(f'Rate for {currency_name} to {currency.rate.base_currency}')
            plt.ylabel(f'{currency_name} rate')
            plt.xlabel('Date')
            image_name = f'{uuid4().hex}.png'
            plt.savefig(f'media/graphs/{image_name}', format="png")
            graph = CurrencyGraph.objects.filter(currency_name=currency_name).first()
            if graph:
                graph.image.delete(save=False)
                graph.image = f'graphs/{image_name}'
                graph.save()
            else:
                CurrencyGraph.objects.create(currency_name=currency_name, image=f'graphs/{image_name}')
            plt.clf()
    plt.close()
