# Generated by Django 3.1.1 on 2020-09-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postit', '0002_auto_20200919_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]