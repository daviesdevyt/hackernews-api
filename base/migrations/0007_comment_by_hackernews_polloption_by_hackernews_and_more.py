# Generated by Django 4.0.4 on 2022-09-27 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_comment_by_hackernews_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='by_hackernews',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='polloption',
            name='by_hackernews',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='by_hackernews',
            field=models.BooleanField(default=True),
        ),
    ]