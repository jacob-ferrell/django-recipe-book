# Generated by Django 4.1.4 on 2023-01-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_favorite_label_favorite_share_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='unit',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='text',
            field=models.TextField(default='poop'),
            preserve_default=False,
        ),
    ]
