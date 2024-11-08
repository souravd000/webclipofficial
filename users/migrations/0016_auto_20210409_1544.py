# Generated by Django 2.2.4 on 2021-04-09 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20210326_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='QR_Snap',
            field=models.ImageField(default='qrdefault.jpg', upload_to='QR_Snap'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gif',
            field=models.FileField(default=False, upload_to='profile_gif'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True),
        ),
    ]
