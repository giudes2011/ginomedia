# Generated by Django 4.2.8 on 2023-12-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='immagine_profilo',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]