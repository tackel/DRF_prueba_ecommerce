# Generated by Django 4.0.4 on 2022-10-19 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_orderdetail_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.CharField(auto_created=True, max_length=2000, primary_key=True, serialize=False),
        ),
    ]
