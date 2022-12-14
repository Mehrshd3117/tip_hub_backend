# Generated by Django 4.1 on 2022-09-12 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_rename_desc_video_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='ادرس آی پی')),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='views',
        ),
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.ManyToManyField(blank=True, to='video.ipaddress', verbose_name='بازدیدها'),
        ),
    ]
