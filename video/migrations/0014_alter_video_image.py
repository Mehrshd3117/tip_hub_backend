# Generated by Django 4.1 on 2022-09-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_alter_video_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='image',
            field=models.ImageField(upload_to='videos/image/', verbose_name='عکس کاور فیلم'),
        ),
    ]
