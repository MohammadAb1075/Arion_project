# Generated by Django 2.2.4 on 2019-09-08 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0003_auto_20190908_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='internshipPlace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShipPlace'),
        ),
        migrations.AlterField(
            model_name='request',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student'),
        ),
        migrations.AlterField(
            model_name='request',
            name='title',
            field=models.CharField(max_length=31),
        ),
    ]
