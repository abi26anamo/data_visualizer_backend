# Generated by Django 5.0.3 on 2024-03-08 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserUploadedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'User uploaded data',
                'db_table': 'user_uploaded_data',
            },
        ),
        migrations.CreateModel(
            name='TimeValuePair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('user_uploaded_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_value_pairs', to='data_importer.useruploadeddata')),
            ],
            options={
                'db_table': 'time_value_pair',
            },
        ),
    ]
