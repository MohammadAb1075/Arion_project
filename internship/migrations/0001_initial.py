# Generated by Django 2.2.4 on 2019-09-25 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choosing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namecity', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='InternShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentFinalReport', models.TextField()),
                ('studentObjectionText', models.TextField()),
                ('studentObjectionDate', models.DateTimeField()),
                ('supervisorReportUploadUrl', models.TextField()),
                ('internShipState', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='InternShipPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameplace', models.CharField(max_length=127)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('internShipWebSite', models.CharField(blank=True, max_length=127, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.City')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namestate', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportDate', models.DateTimeField()),
                ('weekNumber', models.IntegerField()),
                ('reportTitle', models.CharField(max_length=63)),
                ('reportText', models.TextField()),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyConfirmarion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekNumber', models.IntegerField()),
                ('supervisorAttendanCeconfirmation', models.BooleanField(default=False)),
                ('supervisorReportConfirmation', models.BooleanField(default=False)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
            ],
        ),
        migrations.CreateModel(
            name='Student_InternShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gtgrade', models.FloatField()),
                ('gtgradeconfirmation', models.BooleanField()),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester'), ('3', 'Summer')], max_length=15)),
                ('title', models.CharField(max_length=31)),
                ('comment', models.TextField(blank=True, null=True)),
                ('state', models.IntegerField(default=0)),
                ('agreementUploadedUrl', models.TextField(blank=True, null=True)),
                ('reqdate', models.DateTimeField()),
                ('reqhash', models.TextField(blank=True, null=True)),
                ('internshipPlace', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShipPlace')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion', models.BooleanField(blank=True, null=True)),
                ('seenDate', models.DateTimeField(blank=True, null=True)),
                ('opinionDate', models.DateTimeField(blank=True, null=True)),
                ('opinionText', models.TextField(blank=True, null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orequest', to='internship.Request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Operson', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=31)),
                ('email', models.EmailField(max_length=254)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.Request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='internship',
            name='gtOpinion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.Opinion'),
        ),
        migrations.AddField(
            model_name='internship',
            name='guideTeacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.Choosing'),
        ),
        migrations.AddField(
            model_name='internship',
            name='internshiphead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternshipHead'),
        ),
        migrations.AddField(
            model_name='internship',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.State'),
        ),
        migrations.AddField(
            model_name='choosing',
            name='gtOpinion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.Opinion'),
        ),
        migrations.AddField(
            model_name='choosing',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student'),
        ),
        migrations.AddField(
            model_name='choosing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AttendanceTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('weekNumber', models.IntegerField()),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
            ],
        ),
    ]
