# Generated by Django 4.1.4 on 2023-01-28 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_instruction'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]