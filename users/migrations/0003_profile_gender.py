# Generated by Django 2.2.4 on 2019-09-27 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190926_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'FeMale'), ('Custom', 'Custom')], default='', max_length=6),
        ),
    ]