from rest_framework import serializers

from apps.currency.models import Rate


class RateForExchangePurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'

    def to_representation(self, instance):
        data = {
            currency.name: currency.rate_to_base_currency
            for currency in instance.currencies.all()
        }
        data.update({
            'base_currency': instance.base_currency
        })
        return data
