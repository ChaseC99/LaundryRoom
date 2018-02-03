# Generated by Django 2.0.2 on 2018-02-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=64)),
                ('min_time', models.IntegerField()),
                ('max_time', models.IntegerField()),
                ('room', models.CharField(max_length=64)),
                ('admin_id', models.IntegerField()),
                ('last_user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=32)),
                ('start_time', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('machine_id', models.IntegerField()),
            ],
        ),
    ]
