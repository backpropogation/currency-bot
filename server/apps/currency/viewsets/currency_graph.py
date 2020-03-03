from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.currency.models import CurrencyGraph
from apps.currency.serializers import CurrencyGraphSerializer


class CurrencyGraphViewset(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CurrencyGraphSerializer
    queryset = CurrencyGraph.objects.all()
    lookup_field = 'currency_name'
