# Generated by Django 2.1.5 on 2019-04-12 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gnumonitor', '0006_auto_20190412_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='interval',
        ),
    ]