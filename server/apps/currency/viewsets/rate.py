from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.currency.models import Rate
from apps.currency.serializers import RateSerializer, ExchangeCurrenciesSerializer
from apps.currency.utils import Exchanger


class RateViewSet(viewsets.ViewSet):
    parser_classes = (JSONParser,)

    def list(self, request):
        latest_rate = cache.get(settings.LATEST_RATE, None)
        if latest_rate:
            return Response(latest_rate)
        else:
            return Response(RateSerializer(Rate.objects.last()).data)

    @action(detail=False, methods=('post',))
    def exchange(self, request):
        currencies_to_exchange = ExchangeCurrenciesSerializer(data=request.data)
        currencies_to_exchange.is_valid(raise_exception=True)
        return Response(Exchanger.exchange(**currencies_to_exchange.data))
