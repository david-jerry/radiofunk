# Generated by Django 3.2.12 on 2022-03-22 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='podcast',
            field=models.ManyToManyField(default=None, related_name='playlist_podcast', to='podcast.Podcast'),
        ),
    ]
