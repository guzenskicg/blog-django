# Generated by Django 4.2.23 on 2025-06-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0003_menulink_site_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, default='', null=True, upload_to='site_setup/favicon/%Y/%m/'),
        ),
    ]
