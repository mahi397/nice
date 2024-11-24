# Generated by Django 5.1.3 on 2024-11-20 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cruise_management', '0002_authtokentoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenBlacklistBlacklistedtoken',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('blacklisted_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'token_blacklist_blacklistedtoken',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TokenBlacklistOutstandingtoken',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('token', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('expires_at', models.DateTimeField()),
                ('jti', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'token_blacklist_outstandingtoken',
                'managed': False,
            },
        ),
    ]