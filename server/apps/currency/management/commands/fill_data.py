from django.core.management.base import BaseCommand

from apps.currency.tasks import update_rates, draw_graphs


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_rates.apply()
        draw_graphs.apply()
