# Generated by Django 2.2.4 on 2019-08-31 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0003_auto_20190831_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internshipform',
            name='internShipWebSite',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
    ]