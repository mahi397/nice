# Generated by Django 5.1.3 on 2024-11-26 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cruise_management', '0005_authgroup_authgrouppermissions_authpermission_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_profile',
                'managed': False,
            },
        ),
    ]