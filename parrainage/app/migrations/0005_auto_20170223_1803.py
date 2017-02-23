# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_usersettings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AlterField(
            model_name='elu',
            name='role',
            field=models.CharField(choices=[('M', 'Maire'), ('CD', 'Conseiller départemental'), ('CR', 'Conseiller régional'), ('D', 'Député'), ('S', 'Sénateur'), ('DE', 'Député européen'), ('A', 'Autre mandat')], max_length=2),
        ),
        migrations.AlterField(
            model_name='elu',
            name='status',
            field=models.IntegerField(db_index=True, default=1, choices=[(1, "Rien n'a été fait"), (2, 'Démarches en cours'), (3, "Charlotte doit recontacter l'élu"), (10, 'Parrainage refusé'), (20, 'Parrainage accepté')]),
        ),
    ]
