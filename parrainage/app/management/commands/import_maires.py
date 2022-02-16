# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse
import csv

from django.core.management.base import BaseCommand

from parrainage.app.models import Elu
from parrainage.app.rne import parse_elu, met_a_jour_coordonnees_elus

class Command(BaseCommand):
    help = 'Importer les données sur les maires et les mairies'

    def add_arguments(self, parser):
        parser.add_argument('maires', help='chemin vers rne-maires.csv',
                            type=argparse.FileType(mode='r', encoding='utf-8'))
        parser.add_argument('mairies', help='chemin vers mairies.csv',
                            type=argparse.FileType(mode='r', encoding='utf-8'))

    def handle(self, *args, **kwargs):
        tsv_maires = csv.DictReader(kwargs['maires'], delimiter="\t")
        elus = []
        for row in tsv_maires:
            elu = parse_elu(row)
            elus.append(elu)
        Elu.objects.bulk_create(elus)

        csv_mairies = csv.DictReader(kwargs['mairies'], delimiter=",")
        for row in csv_mairies:
            met_a_jour_coordonnees_elus(row)
