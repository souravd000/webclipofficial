# Generated by Django 2.2.4 on 2020-02-15 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20200213_1945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date_posted', 'title']},
        ),
    ]
