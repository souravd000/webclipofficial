# Generated by Django 2.2.4 on 2021-06-23 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20210622_1831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Disable_Messenger_ID',
            new_name='Enable_page_setup',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Digital_Bank_Name_With_Account_Number',
            new_name='Payment_ID',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='restrict_contacts',
            new_name='gender_deactivate',
        ),
        migrations.AddField(
            model_name='profile',
            name='relationship_deactivate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Bio',
            field=models.CharField(default='', max_length=300),
        ),
    ]