# Generated by Django 3.1.6 on 2021-02-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0003_auto_20210218_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='mandatory',
            field=models.BooleanField(default=True),
        ),
    ]
