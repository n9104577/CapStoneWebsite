# Generated by Django 2.0.2 on 2018-10-12 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squashApp', '0004_auto_20181012_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='videodata',
            name='processedVideoFile',
            field=models.FileField(null=True, upload_to='processedVideos/', verbose_name=''),
        ),
    ]
