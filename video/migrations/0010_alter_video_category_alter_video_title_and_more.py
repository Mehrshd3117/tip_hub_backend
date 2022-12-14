# Generated by Django 4.1 on 2022-09-15 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_alter_video_slug_category_video_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ManyToManyField(to='video.category', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=225, unique=True, verbose_name='عنوان ویدیو'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='videos/', verbose_name=' ویدیو'),
        ),
    ]
