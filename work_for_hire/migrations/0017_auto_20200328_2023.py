# Generated by Django 3.0.4 on 2020-03-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0016_auto_20200328_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_chat',
            name='created_by',
            field=models.TimeField(auto_now=True),
        ),
    ]
