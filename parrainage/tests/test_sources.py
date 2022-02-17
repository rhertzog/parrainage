from datetime import date

import pytest


TSV_RNE_MAIRES = """\
Code du département	Libellé du département	Code de la collectivité à statut particulier	Libellé de la collectivité à statut particulier	Code de la commune	Libellé de la commune	Nom de l'élu	Prénom de l'élu	Code sexe	Date de naissance	Code de la catégorie socio-professionnelle	Libellé de la catégorie socio-professionnelle	Date de début du mandat	Date de début de la fonction
01	Ain			01001	L'Abergement-Clémenciat	BOULON	Daniel	M	04/03/1951	74	Ancien cadre	18/05/2020	26/05/2020
"""


@pytest.fixture
def row_rne_maires():
    from parrainage.app.sources.rne import read_tsv

    reader = read_tsv(TSV_RNE_MAIRES.splitlines())
    return list(reader)[0]


def test_tsv_rne_maires(row_rne_maires):
    assert row_rne_maires == {
        "Code de la catégorie socio-professionnelle": "74",
        "Code de la collectivité à statut particulier": "",
        "Code de la commune": "01001",
        "Code du département": "01",
        "Code sexe": "M",
        "Date de début de la fonction": "26/05/2020",
        "Date de début du mandat": "18/05/2020",
        "Date de naissance": "04/03/1951",
        "Libellé de la catégorie socio-professionnelle": "Ancien cadre",
        "Libellé de la collectivité à statut particulier": "",
        "Libellé de la commune": "L'Abergement-Clémenciat",
        "Libellé du département": "Ain",
        "Nom de l'élu": "BOULON",
        "Prénom de l'élu": "Daniel",
    }


class TestParseElu:
    def test_parse_maire(self, row_rne_maires):
        from parrainage.app.sources.rne import parse_elu

        elu = parse_elu(row_rne_maires, role="M")
        assert elu.first_name == "Daniel"
        assert elu.family_name == "BOULON"
        assert elu.gender == "H"
        assert elu.birthdate == date(1951, 3, 4)
        assert elu.role == "M"  # maire
        assert elu.comment == "Catégorie socio-professionnelle: Ancien cadre"
        assert elu.department == "01"
        assert elu.city == "L'Abergement-Clémenciat"
        assert elu.city_code == "01001"


CSV_ANNUAIRE = """\
codeInsee,CodePostal,NomOrganisme,NomCommune,Email,Téléphone,Url,Adresse,Latitude,Longitude,dateMiseAJour
01001,01400,Mairie de L'Abergement-Clémenciat,L'Abergement-Clémenciat,mairieabergementclemenciat@wanadoo.fr,+33 4 74 24 03 08,http://example.org,Le Village,46.151676178,4.92007112503,2014-12-04
"""


@pytest.fixture
def row_annuaire():
    from parrainage.app.sources.annuaire import read_csv

    reader = read_csv(CSV_ANNUAIRE.splitlines())
    return list(reader)[0]


def test_csv(row_annuaire):
    assert row_annuaire == {
        "Adresse": "Le Village",
        "CodePostal": "01400",
        "Email": "mairieabergementclemenciat@wanadoo.fr",
        "Latitude": "46.151676178",
        "Longitude": "4.92007112503",
        "NomCommune": "L'Abergement-Clémenciat",
        "NomOrganisme": "Mairie de L'Abergement-Clémenciat",
        "Téléphone": "+33 4 74 24 03 08",
        "Url": "http://example.org",
        "codeInsee": "01001",
        "dateMiseAJour": "2014-12-04",
    }


@pytest.mark.django_db
def test_met_a_jour_coordonnees_elus(row_rne_maires, row_annuaire):
    from parrainage.app.sources.rne import parse_elu
    from parrainage.app.sources.annuaire import met_a_jour_coordonnees_elus

    elu = parse_elu(row_rne_maires, role="M")
    assert elu.public_email == ""
    assert elu.public_phone == ""
    assert elu.public_website == ""
    assert elu.city_address == ""
    assert elu.city_zipcode == ""
    assert elu.city_latitude == ""
    assert elu.city_longitude == ""

    elu.save()

    met_a_jour_coordonnees_elus(row_annuaire)

    elu.refresh_from_db()
    assert elu.public_email == "mairieabergementclemenciat@wanadoo.fr"
    assert elu.public_phone == "+33 4 74 24 03 08"
    assert elu.public_website == "http://example.org"
    assert elu.city_address == "Le Village"
    assert elu.city_zipcode == "01400"
    assert elu.city_latitude == "46.151676178"
    assert elu.city_longitude == "4.92007112503"
