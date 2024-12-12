# Generated by Django 5.1.3 on 2024-11-26 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cruise_management', '0007_alter_userprofile_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='MmsUserProfile',
            fields=[
                ('profileid', models.AutoField(primary_key=True, serialize=False)),
                ('phonenumber', models.CharField(max_length=15)),
                ('dateofbirth', models.DateField()),
            ],
            options={
                'db_table': 'mms_user_profile',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.DeleteModel(
            name='TokenBlacklistBlacklistedtoken',
        ),
        migrations.DeleteModel(
            name='TokenBlacklistOutstandingtoken',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]