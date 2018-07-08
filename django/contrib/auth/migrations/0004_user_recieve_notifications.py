# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0003_auto_20141211_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='recieve_notifications',
            field=models.BooleanField(default=True, verbose_name='Recieve Notifications'),
            preserve_default=True,
        ),
    ]
