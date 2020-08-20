# Generated by Django 2.2.7 on 2020-08-19 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_manga_integration', '0016_auto_20200819_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermangareadingsettings',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.Manga'),
        ),
        migrations.AlterField(
            model_name='usermangareadingsettings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]