# Generated by Django 3.0.4 on 2020-03-23 07:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_title', models.CharField(max_length=100)),
                ('order_pricing', models.IntegerField()),
                ('requirement', models.CharField(max_length=1000)),
                ('requirement_assets', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
