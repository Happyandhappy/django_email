# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0040_auto_20170521_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='EasyPayLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='partialtaskpay',
            name='easypay_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Easypay code', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='easypay_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Easypay code', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentahead',
            name='from_date',
            field=models.DateField(verbose_name='From date'),
            preserve_default=True,
        ),
    ]
