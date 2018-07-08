# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('document', models.FileField(upload_to=b'', verbose_name='document')),
                ('visible_to_groups', models.ManyToManyField(to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
