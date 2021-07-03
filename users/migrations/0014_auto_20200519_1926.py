# Generated by Django 2.2.4 on 2020-05-19 19:26

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20200519_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Cover_Video',
            field=models.FileField(default='default.mp4', upload_to='cover_videos', validators=[users.validators.file_size, users.validators.File_format]),
        ),
    ]
