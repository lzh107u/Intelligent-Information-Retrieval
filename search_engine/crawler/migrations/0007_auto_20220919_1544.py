# Generated by Django 3.2.5 on 2022-09-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0006_auto_20220919_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubmedpost',
            name='code',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='relwordinmed',
            name='istitle',
            field=models.BooleanField(default=False),
        ),
    ]