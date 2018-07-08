# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0028_auto_20150223_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartialTaskPay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(verbose_name='Price', max_digits=8, decimal_places=2)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'ordering': ('created_at',),
                'verbose_name': 'task partial pay',
                'verbose_name_plural': 'task partial pays',
            },
            bases=(models.Model,),
        ),
    ]
