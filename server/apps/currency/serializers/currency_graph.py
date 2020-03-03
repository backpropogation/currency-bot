from rest_framework import serializers

from apps.currency.models import CurrencyGraph


class CurrencyGraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyGraph
        fields = ('image',)
