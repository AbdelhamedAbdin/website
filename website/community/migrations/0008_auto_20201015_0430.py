# Generated by Django 3.1.1 on 2020-10-15 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20201015_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userasking',
            name='ask_slug',
            field=models.SlugField(allow_unicode=True, max_length=100),
        ),
    ]