# Generated by Django 2.2.7 on 2020-08-19 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manga_integration', '0014_usermangareadingsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermangareadingsettings',
            name='reading_mode',
            field=models.CharField(choices=[['SINGLE_PAGE', 'SINGLE_PAGE'], ['WEBTOON', 'WEBTOON']], max_length=12),
        ),
    ]
