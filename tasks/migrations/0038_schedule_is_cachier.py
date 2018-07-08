# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0037_auto_20150917_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='is_cachier',
            field=models.BooleanField(default=False, verbose_name='Is real cachier'),
            preserve_default=True,
        ),
    ]
