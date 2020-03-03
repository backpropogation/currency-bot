from rest_framework import serializers

from apps.currency.models import Rate
from apps.currency.serializers.currency import CurrencySerializer


class RateSerializer(serializers.ModelSerializer):
    currencies = CurrencySerializer(many=True)
    date = serializers.DateTimeField(format='%d.%m.%Y at %H:%M:%S')

    class Meta:
        model = Rate
        fields = (
            'date',
            'currencies',
            'base_currency'
        )
