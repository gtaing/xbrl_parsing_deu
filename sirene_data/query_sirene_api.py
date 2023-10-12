import os

import requests
import pandas as pd


def get_siren_info(siren_number, ref_code_naf):
    # Remarque : l'API Sirene de l'insee autorise 30 requêtes/minutes
    # Il faut créer une application sur le site de l'INSEE et récupérer un token pour exécuter les requêtes
    # Il existe également un générateur de jetons d'accès

    url = f'https://api.insee.fr/entreprises/sirene/V3/siren?q=siren:{siren_number}'
    token = ''
    json = requests.get(url=url, headers={'Authorization': f'Bearer {token}'}).json()

    # Jointure entre les données entreprises et le code NAF pour obtenir l'activité de l'entreprise
    out = pd.DataFrame(json['unitesLegales'][0].get('periodesUniteLegale'))
    out = out.rename(columns={'activitePrincipaleUniteLegale': 'Code'})
    out = pd.merge(out, ref_code_naf, on='Code')

    return out


if __name__ == "__main__":
    # Lien vers la DOC Insee Sirene : https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee#!/UniteLegale/findSirenByQ

    # Préparation des données NAF
    ref_code_naf = pd.read_excel('int_courts_naf_rev_2.xls')
    ref_code_naf.columns = ref_code_naf.columns.str.strip()
    ref_code_naf = ref_code_naf[['Code',
                                 'Intitulés de la  NAF rév. 2, version finale',
                                 'Intitulés NAF rév. 2, \nen 65 caractères']]

    # Récupérer les informations sur un code Siren précis
    df = get_siren_info(siren_number='542052766', ref_code_naf=ref_code_naf)
    df.to_excel('ask_siren_chanel.xlsx', index=False)
