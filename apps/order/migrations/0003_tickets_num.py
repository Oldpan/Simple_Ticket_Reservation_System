# Generated by Django 2.0 on 2017-12-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20171211_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='num',
            field=models.CharField(default='K100', max_length=10, verbose_name='车票编号'),
        ),
    ]
