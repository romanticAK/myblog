# Generated by Django 3.0.4 on 2020-03-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200324_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(upload_to='banner/', verbose_name='轮播图'),
        ),
    ]
