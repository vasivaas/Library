# Generated by Django 3.0.4 on 2020-03-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_book_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='genre_image',
            field=models.ImageField(blank=True, upload_to='picture/%Y/%m/%d/'),
        ),
    ]