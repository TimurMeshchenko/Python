# Generated by Django 4.2.1 on 2023-05-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remanga', '0002_title_avg_rating_title_dir_name_title_rus_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
    ]
