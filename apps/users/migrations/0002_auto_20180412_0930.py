# Generated by Django 2.0.4 on 2018-04-12 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagecode',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chartsite/captcha', verbose_name='图片'),
        ),
    ]
