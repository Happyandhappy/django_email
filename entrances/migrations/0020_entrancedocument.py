# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0019_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('document', models.FileField(upload_to=b'entrancedocuments/%Y/%m', verbose_name='document')),
                ('entrance', models.ForeignKey(verbose_name='entrance', to='entrances.Entrance')),
            ],
            options={
                'verbose_name': 'uploaded document',
                'verbose_name_plural': 'uploaded documents',
            },
            bases=(models.Model,),
        ),
    ]
