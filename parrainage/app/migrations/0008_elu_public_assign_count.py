# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_elu_private_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='elu',
            name='public_assign_count',
            field=models.IntegerField(default=0, db_index=True),
        ),
    ]
