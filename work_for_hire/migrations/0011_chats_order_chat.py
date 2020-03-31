# Generated by Django 3.0.4 on 2020-03-27 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_for_hire', '0010_delete_order_chats'),
    ]

    operations = [
        migrations.CreateModel(
            name='chats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1200)),
            ],
        ),
        migrations.CreateModel(
            name='order_chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=200)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_for_hire.chats')),
            ],
        ),
    ]
