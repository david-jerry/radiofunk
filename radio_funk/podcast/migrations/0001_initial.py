# Generated by Django 3.2.12 on 2022-03-18 00:06

import autoslug.fields
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import radio_funk.utils.fields
import radio_funk.utils.storages
import stdimage.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EpisodeGift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Episode Gift',
                'verbose_name_plural': 'Episode Gifts',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Episodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', radio_funk.utils.fields.UUIDField(blank=True, editable=False, max_length=36, unique=True, verbose_name='ID')),
                ('audio', models.FileField(blank=True, upload_to=radio_funk.utils.storages.get_norm_audio_upload_folder, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3'])], verbose_name='AudioFile')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique='True', verbose_name='slug')),
                ('description', tinymce.models.HTMLField(verbose_name='Episode Description')),
                ('subtitle', models.CharField(help_text='Looks best if only a few words, like a tagline.', max_length=255, verbose_name='subtitle')),
                ('image', stdimage.models.StdImageField(blank=True, help_text='\n                An episode must have 700 x 700 pixel cover art in JPG or PNG\n                format using RGB color space. See our technical spec for\n                details. To be eligible for featuring on iTunes Stores,\n                choose an attractive, original, and square JPEG (.jpg) or\n                PNG (.png) image at a size of 1400x1400 pixels. The image\n                will be scaled down to 50x50 pixels at smallest in iTunes.\n                For reference see the <a\n                href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes\n                Podcast specs</a>.<br /><br /> For episode artwork to\n                display in iTunes, image must be <a\n                href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n                saved to file\'s <strong>metadata</strong></a> before\n                enclosure uploading!', upload_to=radio_funk.utils.storages.get_episode_upload_folder)),
                ('explicit', models.PositiveSmallIntegerField(choices=[(1, 'yes'), (2, 'no'), (3, 'clean'), (4, 'kids')], default=1, help_text='Audience this content should be shown to. Explicit determines this episode not being shown to viewers under 18 years of age.', verbose_name='explicit')),
                ('enable_comments', models.BooleanField(default=True)),
                ('published', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='published')),
            ],
            options={
                'verbose_name': 'Podcast Episode',
                'verbose_name_plural': 'Podcast Episodes',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', tinymce.models.HTMLField(verbose_name='Gift Story')),
                ('image', stdimage.models.StdImageField(blank=True, upload_to='gift/gif')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
            ],
            options={
                'verbose_name': 'Gift Item',
                'verbose_name_plural': 'Gift Items',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique='True', verbose_name='slug')),
                ('description', tinymce.models.HTMLField(verbose_name='Playlist Description')),
                ('private', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Podcast Playlist',
                'verbose_name_plural': 'Podcast Playlists',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', radio_funk.utils.fields.UUIDField(blank=True, editable=False, max_length=36, unique=True, verbose_name='id')),
                ('publish', models.BooleanField(default=True, verbose_name='published')),
                ('ttl', models.PositiveIntegerField(default=1440, help_text='``Time to Live,`` the number of minutes a channel can be\n        cached before refreshing.', verbose_name='ttl')),
                ('author_text', models.CharField(help_text="\n            This tag contains the name of the person or company that is most\n            widely attributed to publishing the Podcast and will be\n            displayed immediately underneath the title of the Podcast.\n            The suggested format is: 'email@example.com (Full Name)'\n            but 'Full Name' only, is acceptable. Multiple authors\n            should be comma separated.", max_length=255, verbose_name='Featured Personalities')),
                ('name', models.CharField(max_length=255, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique='True', verbose_name='slug')),
                ('description', tinymce.models.HTMLField(verbose_name='Show Description')),
                ('subtitle', models.CharField(help_text='Looks best if only a few words, like a tagline.', max_length=255, verbose_name='subtitle')),
                ('image', stdimage.models.StdImageField(blank=True, help_text='\n                A podcast must have 700 x 700 pixel cover art in JPG or PNG\n                format using RGB color space. See our technical spec for\n                details. To be eligible for featuring on iTunes Stores,\n                choose an attractive, original, and square JPEG (.jpg) or\n                PNG (.png) image at a size of 1400x1400 pixels. The image\n                will be scaled down to 50x50 pixels at smallest in iTunes.\n                For reference see the <a\n                href="http://www.apple.com/itunes/podcasts/specs.html#metadata">iTunes\n                Podcast specs</a>.<br /><br /> For episode artwork to\n                display in iTunes, image must be <a\n                href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">\n                saved to file\'s <strong>metadata</strong></a> before\n                enclosure uploading!', upload_to=radio_funk.utils.storages.get_show_upload_folder)),
                ('address', models.TextField(blank=True, null=True)),
                ('explicit', models.PositiveSmallIntegerField(choices=[(1, 'yes'), (2, 'no'), (3, 'clean'), (4, 'kids')], default=2, help_text='Audience this content should be shown to. Explicit determines this episode not being shown to viewers under 18 years of age.', verbose_name='explicit')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('enable_comments', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Podcast Show',
                'verbose_name_plural': 'Podcast Shows',
                'ordering': ['-created'],
                'managed': True,
            },
        ),
    ]
