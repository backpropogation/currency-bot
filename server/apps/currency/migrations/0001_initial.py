from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=4)),
                ('image', models.ImageField(upload_to='graphs')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('base_currency', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_to_base_currency', models.DecimalField(decimal_places=2, max_digits=20)),
                ('name', models.CharField(max_length=4)),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currencies', to='currency.Rate')),
            ],
        ),
    ]
