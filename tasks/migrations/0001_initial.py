# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import select2.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0006_auto_20141112_0944'),
        ('entrances', '0013_auto_20141112_1337'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0002_auto_20141107_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('can_pay', models.BooleanField(default=False, verbose_name='can pay bill')),
                ('can_pay_partial', models.BooleanField(default=False, verbose_name='can pay bill partial')),
                ('price', models.DecimalField(null=True, verbose_name='Price', max_digits=8, decimal_places=2, blank=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is paid')),
                ('from_date', models.DateField(null=True, verbose_name='From date', blank=True)),
                ('to_date', models.DateField(null=True, verbose_name='To date', blank=True)),
                ('common_information', ckeditor.fields.RichTextField(null=True, verbose_name='Common information', blank=True)),
                ('apartment', select2.fields.ForeignKey(verbose_name='Apartment', blank=True, to='entrances.Apartment', null=True)),
                ('assignee', select2.fields.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('document', models.FileField(upload_to=b'taskdocuments/%Y/%m', verbose_name='document')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='documents',
            field=select2.fields.ManyToManyField(to='tasks.TaskDocument', verbose_name='document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='entrance', blank=True, to='entrances.Entrance', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=select2.fields.ForeignKey(verbose_name='priority', to='nomenclatures.Priority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=select2.fields.ForeignKey(verbose_name='task type', to='nomenclatures.TaskType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='template',
            field=select2.fields.ManyToManyField(to='documents.Document', verbose_name='document'),
            preserve_default=True,
        ),
    ]
