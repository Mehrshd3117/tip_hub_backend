# Generated by Django 4.1 on 2022-09-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_alter_video_category_alter_video_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ManyToManyField(related_name='video_category', to='video.category', verbose_name='دسته بندی'),
        ),
    ]
