# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from parrainage.app.models import Elu
from parrainage.app.sources.rne import read_tsv, parse_elu


MANDAT = {
    "CD": "Conseiller départemental",
    "CR": "Conseiller régional",
    "S": "Sénateur",
}

class Command(BaseCommand):
    help = "Importer les données du RNE sur des élus (hors maires)"

    def add_arguments(self, parser):
        parser.add_argument(
            "csvfile",
            help="fichier rne-xxx.csv du RNE",
            type=argparse.FileType(mode="r", encoding="utf-8"),
        )
        parser.add_argument(
            "--mandat", help="Type de mandat", choices=["CD", "CR", "S"], required=True
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        nouveaux_elus = []
        nb_elus_mis_a_jour = 0
        for row in read_tsv(kwargs["csvfile"]):
            elu = parse_elu(row, role=kwargs["mandat"])
            try:
                elu_existant = Elu.objects.get(
                    first_name=elu.first_name,
                    family_name=elu.family_name,
                    birthdate=elu.birthdate,
                )
                if elu_existant.role == elu.role:
                    continue
                else:
                    annotation = "\nAutre mandat: {MANDAT[elu.role]}"
                    if annotation not in elu_existant.comment:
                        elu_existant.comment += annotation
                        elu_existant.save()
                        nb_elus_mis_a_jour += 1
            except Elu.DoesNotExist:
                nouveaux_elus.append(elu)
            except Elu.MultipleObjectsReturned:
                logging.error(
                    "Il y a plusieurs %s %s né(e)s le %s",
                    elu.first_name, elu.family_name, elu.birthdate
                )
        Elu.objects.bulk_create(nouveaux_elus)
        print(f"Ajouté {len(nouveaux_elus)} élus et mis à jour {nb_elus_mis_a_jour} élus existants.")
