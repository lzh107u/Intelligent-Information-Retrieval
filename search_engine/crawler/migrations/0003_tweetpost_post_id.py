# Generated by Django 3.2.5 on 2022-09-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20220916_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetpost',
            name='post_id',
            field=models.IntegerField(default=-1),
        ),
    ]
