# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0004_apartment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='floor',
            field=models.CharField(default=0, max_length=2, verbose_name='Floor', choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5'), (b'6', b'6'), (b'7', b'7'), (b'8', b'8'), (b'9', b'9'), (b'10', b'10'), (b'11', b'11'), (b'12', b'12'), (b'13', b'13'), (b'14', b'14'), (b'15', b'15'), (b'16', b'16'), (b'17', b'17'), (b'18', b'18'), (b'19', b'19'), (b'20', b'20'), (b'21', b'21'), (b'22', b'22'), (b'23', b'23'), (b'24', b'24'), (b'25', b'25'), (b'26', b'26'), (b'27', b'27'), (b'28', b'28'), (b'29', b'29'), (b'30', b'30'), (b'31', b'31'), (b'32', b'32'), (b'33', b'33'), (b'34', b'34'), (b'35', b'35'), (b'36', b'36'), (b'37', b'37'), (b'38', b'38'), (b'39', b'39'), (b'40', b'40'), (b'41', b'41'), (b'42', b'42'), (b'43', b'43'), (b'44', b'44'), (b'45', b'45'), (b'46', b'46'), (b'47', b'47'), (b'48', b'48'), (b'49', b'49'), (b'50', b'50'), (b'51', b'51'), (b'52', b'52'), (b'53', b'53'), (b'54', b'54'), (b'55', b'55'), (b'56', b'56'), (b'57', b'57'), (b'58', b'58'), (b'59', b'59'), (b'60', b'60'), (b'61', b'61'), (b'62', b'62'), (b'63', b'63'), (b'64', b'64'), (b'65', b'65'), (b'66', b'66'), (b'67', b'67'), (b'68', b'68'), (b'69', b'69'), (b'70', b'70'), (b'71', b'71'), (b'72', b'72'), (b'73', b'73'), (b'74', b'74'), (b'75', b'75'), (b'76', b'76'), (b'77', b'77'), (b'78', b'78'), (b'79', b'79'), (b'80', b'80'), (b'81', b'81'), (b'82', b'82'), (b'83', b'83'), (b'84', b'84'), (b'85', b'85'), (b'86', b'86'), (b'87', b'87'), (b'88', b'88'), (b'89', b'89'), (b'90', b'90'), (b'91', b'91'), (b'92', b'92'), (b'93', b'93'), (b'94', b'94'), (b'95', b'95'), (b'96', b'96'), (b'97', b'97'), (b'98', b'98')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartment',
            name='number_of_occupants',
            field=models.CharField(default=2, max_length=2, verbose_name='Number of occupants', choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5'), (b'6', b'6'), (b'7', b'7'), (b'8', b'8'), (b'9', b'9')]),
            preserve_default=True,
        ),
    ]
