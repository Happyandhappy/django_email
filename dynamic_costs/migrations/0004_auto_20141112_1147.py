# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0003_auto_20141112_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccost',
            name='common_information',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Common information', blank=True),
            preserve_default=True,
        ),
    ]
