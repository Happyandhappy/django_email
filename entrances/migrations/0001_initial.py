# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('google_maps', models.URLField(max_length=2048, null=True, verbose_name='Google maps', blank=True)),
                ('tax_form', ckeditor.fields.RichTextField(null=True, verbose_name='Tax form', blank=True)),
                ('tax_amount', models.DecimalField(null=True, verbose_name='Tax amount', max_digits=8, decimal_places=2, blank=True)),
                ('contract_date', models.DateField(verbose_name='Contract date')),
                ('protocol_date', models.DateField(verbose_name='Protocol date')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'task type',
                'verbose_name_plural': 'task types',
            },
            bases=(models.Model,),
        ),
    ]
