# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0002_auto_20141110_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrance',
            name='common_information',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Common information', blank=True),
            preserve_default=True,
        ),
    ]
