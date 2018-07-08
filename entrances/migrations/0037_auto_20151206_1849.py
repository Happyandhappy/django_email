# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0036_apartment_pay_online'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceKasa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'EntranceKasa',
                'verbose_name_plural': 'EntranceKasa',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZipEntrance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'ZipEntrances',
                'verbose_name_plural': 'ZipEntrance',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entrance',
            name='dont_sent_emails',
            field=models.BooleanField(default=False, verbose_name='Dont send notification emails'),
            preserve_default=True,
        ),
    ]
