# Generated by Django 3.2.16 on 2024-10-01 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_post_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
