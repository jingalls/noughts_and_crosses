# Generated by Django 4.2.18 on 2025-02-08 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_remove_move_move_move_x_move_y'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='state',
            field=models.JSONField(default=list),
        ),
    ]
