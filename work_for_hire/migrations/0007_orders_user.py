# Generated by Django 3.0.4 on 2020-03-23 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0006_remove_orders_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.CharField(default='s', max_length=100),
            preserve_default=False,
        ),
    ]
