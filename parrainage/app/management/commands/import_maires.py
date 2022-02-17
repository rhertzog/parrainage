# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse

from django.core.management.base import BaseCommand

from parrainage.app.models import Elu
from parrainage.app.sources.rne import read_tsv, parse_elu
from parrainage.app.sources.annuaire import read_csv, met_a_jour_coordonnees_elus


class Command(BaseCommand):
    help = "Importer les données sur les maires et les mairies"

    def add_arguments(self, parser):
        parser.add_argument(
            "maires",
            help="fichier rne-maires.csv du RNE",
            type=argparse.FileType(mode="r", encoding="utf-8"),
        )
        parser.add_argument(
            "mairies",
            help="chemin vers mairies.csv",
            type=argparse.FileType(mode="r", encoding="utf-8"),
        )

    def handle(self, *args, **kwargs):
        elus = []
        for row in read_tsv(kwargs["maires"]):
            elu = parse_elu(row, role="M")
            elus.append(elu)
        Elu.objects.bulk_create(elus)

        csv_mairies = read_csv(kwargs["mairies"])
        for row in csv_mairies:
            met_a_jour_coordonnees_elus(row)
