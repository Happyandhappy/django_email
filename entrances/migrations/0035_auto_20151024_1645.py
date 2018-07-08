# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0034_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='common_information',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Common information', blank=True),
            preserve_default=True,
        ),
    ]
