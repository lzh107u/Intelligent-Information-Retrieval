# Generated by Django 3.2.5 on 2022-09-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0007_auto_20220919_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medauthor',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
