from django.db import migrations

from apps.currency.tasks import update_rates, draw_graphs


def init_models(apps, schema_editor):
    update_rates.apply()
    draw_graphs.apply()


class Migration(migrations.Migration):
    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_models)
    ]
