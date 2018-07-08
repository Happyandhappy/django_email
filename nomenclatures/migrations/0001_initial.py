# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.BooleanField(max_length=255, verbose_name='Title')),
                ('can_pay', models.BooleanField(verbose_name='can pay bill')),
                ('can_pay_partial', models.BooleanField(verbose_name='can pay bill partial')),
                ('for_cachiers', models.BooleanField(verbose_name='can cachier add this task type')),
            ],
            options={
                'verbose_name': 'task type',
                'verbose_name_plural': 'task types',
            },
            bases=(models.Model,),
        ),
    ]
