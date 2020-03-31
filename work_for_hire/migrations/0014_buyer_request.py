# Generated by Django 3.0.4 on 2020-03-28 11:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0013_auto_20200327_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='buyer_request',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
                ('rst', models.CharField(max_length=1200)),
                ('files', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]