# Generated by Django 2.0.2 on 2018-10-25 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squashApp', '0009_auto_20181025_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='videodata',
            name='player1HeatMapVideo',
            field=models.FileField(null=True, upload_to='processedVideos/', verbose_name=''),
        ),
        migrations.AddField(
            model_name='videodata',
            name='player2HeatMapVideo',
            field=models.FileField(null=True, upload_to='processedVideos/', verbose_name=''),
        ),
    ]
