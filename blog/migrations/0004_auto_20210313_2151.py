# Generated by Django 2.2.5 on 2021-03-13 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210313_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_likes',
            field=models.ManyToManyField(blank=True, default=False, null=True, related_name='likes', to='blog.UserProfileInfo'),
        ),
    ]
