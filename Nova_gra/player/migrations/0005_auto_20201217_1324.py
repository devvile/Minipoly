# Generated by Django 3.0.6 on 2020-12-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0004_player_ready'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='in_game',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
