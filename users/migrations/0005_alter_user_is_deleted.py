# Generated by Django 3.2.15 on 2022-08-17 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220817_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
