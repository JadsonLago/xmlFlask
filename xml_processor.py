import os
import pandas as pd
from lxml import etree

def process_xml_file(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()

    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    invoice_number = root.findtext('.//nfe:ide/nfe:nNF', namespaces=ns)
    issue_date = root.findtext('.//nfe:ide/nfe:dhEmi', namespaces=ns)
    total_value = root.findtext('.//nfe:total/nfe:ICMSTot/nfe:vNF', namespaces=ns)

    return {
        'invoice_number': invoice_number,
        'issue_date': issue_date,
        'total_value': total_value
    }

def process_all_xml_files(folder_path):
    xml_data = []
    for xml_file in os.listdir(folder_path):
        if xml_file.endswith('.xml'):
            file_path = os.path.join(folder_path, xml_file)
            data = process_xml_file(file_path)
            xml_data.append(data)

    df = pd.DataFrame(xml_data)
    return df


from models import NFe

# Função para salvar os dados no banco de dados
def save_to_database(df):
    for _, row in df.iterrows():
        NFe.create(
            invoice_number=row['invoice_number'],
            issue_date=row['issue_date'],
            total_value=row['total_value']
        )

    print('Dados salvos com sucesso!')