# Generated by Django 3.0.6 on 2020-12-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='positions',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
    ]
