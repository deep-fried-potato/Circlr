# Generated by Django 2.1.1 on 2018-12-09 10:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pending_Requests',
            new_name='Friends_Status',
        ),
    ]
