# Generated by Django 2.0 on 2018-01-06 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0003_watch_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watch',
            old_name='user',
            new_name='users',
        ),
    ]