# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0003_auto_20141107_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priorioty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('color', colorful.fields.RGBColorField(verbose_name='Color')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
