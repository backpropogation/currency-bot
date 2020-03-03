from rest_framework.routers import DefaultRouter
from apps.currency.viewsets import CurrencyGraphViewset, RateViewSet

router = DefaultRouter()

router.register('graphs', CurrencyGraphViewset, base_name='graph')
router.register('rates', RateViewSet, base_name='rate')