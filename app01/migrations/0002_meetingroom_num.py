# Generated by Django 2.0 on 2017-12-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingroom',
            name='num',
            field=models.IntegerField(null=True, verbose_name='可容纳人数'),
        ),
    ]
