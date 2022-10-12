# Generated by Django 4.0.4 on 2022-10-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Name of Product')),
                ('price', models.FloatField(default=0, verbose_name='Price of Product')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock of Product')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]