# Generated by Django 3.0.4 on 2020-03-28 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0015_buyer_request_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer_request',
            old_name='files',
            new_name='rst_attach',
        ),
        migrations.AddField(
            model_name='buyer_request',
            name='created_by',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
