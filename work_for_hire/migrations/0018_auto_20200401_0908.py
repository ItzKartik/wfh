# Generated by Django 3.0.4 on 2020-04-01 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0017_auto_20200328_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_chat',
            name='created_by',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
