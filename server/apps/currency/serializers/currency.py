from rest_framework import serializers

from apps.currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('name', 'rate_to_base_currency')



