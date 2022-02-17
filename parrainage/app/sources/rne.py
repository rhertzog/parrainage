from datetime import datetime
import csv

from parrainage.app.models import Elu


def read_tsv(iterable):
    return csv.DictReader(iterable, delimiter="\t")


def parse_elu(row, role):
    """
    Crée un élu à partir d'une ligne d’un fichier du Répertoire National des Élus

    https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/
    """
    gender = "H" if row["Code sexe"] == "M" else "F"
    birthdate = datetime.strptime(row["Date de naissance"], "%d/%m/%Y").date()
    return Elu(
        first_name=row["Prénom de l'élu"],
        family_name=row["Nom de l'élu"],
        gender=gender,
        birthdate=birthdate,
        role=role,
        comment="Catégorie socio-professionnelle: {}".format(
            row["Libellé de la catégorie socio-professionnelle"]
        ),
        department=row.get("Code du département", ""),
        city=row.get("Libellé de la commune", ""),
        # city_size=int(row["Population"]),
        city_code=row.get("Code de la commune", ""),
        # nuance_politique=row["CodeNuancePolitique"],
    )