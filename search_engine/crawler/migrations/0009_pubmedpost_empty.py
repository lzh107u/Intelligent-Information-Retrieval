# Generated by Django 3.2.5 on 2022-09-19 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0008_alter_medauthor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubmedpost',
            name='empty',
            field=models.BooleanField(default=False),
        ),
    ]
