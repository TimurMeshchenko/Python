# Generated by Django 4.2.1 on 2023-05-27 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remanga', '0003_title_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='img_url',
            field=models.CharField(default='', max_length=100),
        ),
    ]
