# Generated by Django 2.1.5 on 2019-04-12 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gnumonitor', '0005_remove_chart_id_chart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='comandline',
            new_name='commandline',
        ),
        migrations.RenameField(
            model_name='data_chart',
            old_name='id_chart',
            new_name='chart_object',
        ),
    ]