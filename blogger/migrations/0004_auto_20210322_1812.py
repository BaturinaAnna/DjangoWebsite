# Generated by Django 3.1.5 on 2021-03-22 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0003_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.TextField(default='NN', max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(default='img1.png', upload_to=''),
        ),
    ]
