import pytest


MAIRES = """\
Code du département\tLibellé du département\tCode de la collectivité à statut particulier\tLibellé de la collectivité à statut particulier\tCode de la commune\tLibellé de la commune\tNom de l'élu\tPrénom de l'élu\tCode sexe\tDate de naissance\tCode de la catégorie socio-professionnelle\tLibellé de la catégorie socio-professionnelle\tDate de début du mandat\tDate de début de la fonction
47\tLot-Et-Garonne\t\t\t47286\tSauméjan\tRIVETTA-BOURRAS\tFrançoise\tF\t02/11/1957\t33\tCadre de la fonction publique\t18/05/2020\t23/05/2020
"""


@pytest.fixture
def elus():
    from parrainage.app.models import Elu
    from parrainage.app.sources.rne import read_tsv, parse_elu

    reader = read_tsv(MAIRES.splitlines())
    elus = [parse_elu(row, role="M") for row in reader]
    Elu.objects.bulk_create(elus)


@pytest.mark.django_db
def test_nom_compose(elus):
    from parrainage.app.management.commands.import_parrainages import trouve_elu

    row = {
        "Civilité": "Mme",
        "Nom": "RIVETTA",
        "Prénom": "Françoise",
        "Mandat": "Maire",
        "Circonscription": "Sauméjan",
        "Département": "Lot-et-Garonne",
        "Candidat": "ARTHAUD Nathalie",
        "Date de publication": "08/02/2022",
    }
    elu = trouve_elu(row)
    assert elu.family_name == "RIVETTA-BOURRAS"
