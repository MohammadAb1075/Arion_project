# Generated by Django 2.2.4 on 2019-09-06 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipplace',
            name='phone',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]