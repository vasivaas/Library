# Generated by Django 3.0.4 on 2020-03-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20200317_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='link',
            field=models.CharField(default='https://python.swaroopch.com', max_length=200),
        ),
    ]