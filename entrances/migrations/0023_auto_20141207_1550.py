# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0022_auto_20141207_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='floor',
            field=models.IntegerField(default=0, max_length=2, verbose_name='Floor', choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10'), (11, b'11'), (12, b'12'), (13, b'13'), (14, b'14'), (15, b'15'), (16, b'16'), (17, b'17'), (18, b'18'), (19, b'19'), (20, b'20')]),
            preserve_default=True,
        ),
    ]
