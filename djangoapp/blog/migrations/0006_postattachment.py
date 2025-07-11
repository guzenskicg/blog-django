# Generated by Django 4.2.23 on 2025-06-27 23:50

from django.db import migrations, models
import django_summernote.utils


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_created_by_post_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Defaults to filename, if left blank', max_length=255, null=True)),
                ('file', models.FileField(upload_to=django_summernote.utils.uploaded_filepath)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Post Attachment',
                'verbose_name_plural': 'Post Attachments',
            },
        ),
    ]
