import os
import pandas as pd
from lxml import etree


def process_xml_file(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()

    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    #dados da nota
    n_nota = root.findtext('.//nfe:ide/nfe:nNF', namespaces=ns)
    data_emit = root.findtext('.//nfe:ide/nfe:dhEmi', namespaces=ns)
    valor_total = root.findtext('.//nfe:total/nfe:ICMSTot/nfe:vNF', namespaces=ns)

    #dados do emitente
    emit = root.find('.//nfe:emit', namespaces=ns)
    emit_cnpj = emit.findtext('./nfe:CNPJ', namespaces=ns)
    emit_nome = emit.findtext('./nfe:xNome', namespaces=ns)
    emit_ie = emit.findtext('./nfe:IE', namespaces=ns)


    return {
        'n_nota': n_nota,
        'data_emit': data_emit,
        'valor_total': valor_total,
        #dados do emitente
        'emit_cnpj': emit_cnpj,
        'emit_nome': emit_nome,
        'emit_ie': emit_ie
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


from models import NFe, Emitente

# Função para salvar os dados no banco de dados
def save_to_database(df):
    for _, row in df.iterrows():


        if not Emitente.select().where(Emitente.emit_cnpj == row['emit_cnpj']).exists():
            Emitente.create(
                emit_cnpj=row['emit_cnpj'],
                emit_nome=row['emit_nome'],
                emit_ie=row['emit_ie']
            )

        if not NFe.select().where(NFe.n_nota == row['n_nota']).exists():
            NFe.create(
                n_nota=row['n_nota'],
                data_emit=row['data_emit'],
                valor_total=row['valor_total'],
                emitente = Emitente.select().where(Emitente.emit_cnpj == row['emit_cnpj']).get()            
            )
        
        

                
    print('Dados salvos com sucesso!')