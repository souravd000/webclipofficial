# Generated by Django 2.2.4 on 2019-11-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='coverpic',
            field=models.ImageField(default='default.jpg', upload_to='cover_pic'),
        ),
    ]
