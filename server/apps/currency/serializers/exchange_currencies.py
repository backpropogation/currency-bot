from rest_framework import serializers
from rest_framework.exceptions import ParseError

from apps.currency.utils import get_currencies_of_latest_rate


class ExchangeCurrenciesSerializer(serializers.Serializer):
    from_currency = serializers.CharField()
    to_currency = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate_amount(self, amount):
        if amount < 0:
            raise ParseError(detail='Amount must be greater than zero.')
        return amount

    def validate(self, attrs):
        currencies_names = get_currencies_of_latest_rate()
        if attrs['from_currency'] in currencies_names and attrs['to_currency'] in currencies_names:
            return attrs
        raise ParseError(detail='Bad currency name.')
