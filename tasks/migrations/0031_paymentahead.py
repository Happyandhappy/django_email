# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from django.conf import settings
import select2.fields
import vhodove.helper


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0029_auto_20150614_1616'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0030_auto_20150329_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentAhead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(default=vhodove.helper.first_day_of_month, verbose_name='From date')),
                ('period', models.IntegerField(verbose_name='Period')),
                ('apartment', smart_selects.db_fields.ChainedForeignKey(verbose_name='Apartment', blank=True, to='entrances.Apartment', null=True)),
                ('assignee', select2.fields.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('entrance', select2.fields.ForeignKey(verbose_name='Entrance', blank=True, to='entrances.Entrance', null=True)),
            ],
            options={
                'ordering': ('from_date',),
                'verbose_name': 'PaymentAhead',
                'verbose_name_plural': 'PaymentAhead',
            },
            bases=(models.Model,),
        ),
    ]
