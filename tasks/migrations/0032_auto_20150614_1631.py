# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from django.conf import settings
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0031_paymentahead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentahead',
            name='apartment',
            field=smart_selects.db_fields.ChainedForeignKey(verbose_name='Apartment', to='entrances.Apartment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentahead',
            name='assignee',
            field=select2.fields.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentahead',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='Entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
    ]
