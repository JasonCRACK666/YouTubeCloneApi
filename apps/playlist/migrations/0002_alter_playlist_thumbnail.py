# Generated by Django 4.2.2 on 2023-08-07 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]