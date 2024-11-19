# Generated by Django 5.1.3 on 2024-11-19 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cruise_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthtokenToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'authtoken_token',
                'managed': False,
            },
        ),
    ]