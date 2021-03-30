# Generated by Django 3.1.7 on 2021-03-26 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogger', '0008_auto_20210325_2212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='views',
            new_name='likes',
        ),
        migrations.AddField(
            model_name='blog',
            name='avatar',
            field=models.ImageField(default='profile.png', upload_to='media/user_photo'),
        ),
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation timestamp')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogger.blog')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]