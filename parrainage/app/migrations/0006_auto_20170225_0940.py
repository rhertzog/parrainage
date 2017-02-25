# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170223_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elu',
            name='status',
            field=models.IntegerField(default=1, db_index=True, choices=[(1, "Rien n'a été fait"), (2, 'Démarches en cours'), (3, "Charlotte doit recontacter l'élu"), (3, "L'élu souhaite être recontacté"), (10, 'Parrainage refusé'), (20, 'Parrainage accepté'), (30, 'Parrainage reçu par le conseil constitutionnel')]),
        ),
    ]
