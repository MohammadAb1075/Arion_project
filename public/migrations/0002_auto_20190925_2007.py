# Generated by Django 2.2.4 on 2019-09-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='phone',
        ),
        migrations.AddField(
            model_name='users',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
