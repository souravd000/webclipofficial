# Generated by Django 2.2.4 on 2021-04-01 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20210326_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='coder',
        ),
        migrations.RemoveField(
            model_name='post',
            name='coder',
        ),
    ]