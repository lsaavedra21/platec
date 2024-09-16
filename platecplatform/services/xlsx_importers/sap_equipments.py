from equipamentos.models import *
from tqdm import tqdm
import os, ipdb
import pandas as pd

# Esse script foi feito para importar a planilha de equipamentos do sap para a base de dados
# Ele filtra os equipamentos inativos, cria se o equipamento se não existir, ou atualiza oque já existe

# Ficou de ser resolvido um bug, caso o equipamento seja excluido do sap, ele vai ser retirado nos filtros, e o equipamento continuará 
# base de dados Platec

def get_eqp_sup_row_df(actual_row, df) -> Equipamento:
    row = df[df['Equipamento'].isin([actual_row['Equip.superior']])]
    for index, _row in row.iterrows():
        return equipments(_row, df)


def equipments(row, df):

    area = departamento = eqp_sup = linha = zona = posto = None
    local_instalacao = row['Loc.instalação'].replace('-', '').split('_')


    if len(str(row['Equip.superior'])) > 0:
        eqp_sup = get_eqp_sup_row_df(actual_row=row, df=df)

    
    try:
        planta = Planta.objects.get(codigo=local_instalacao[0])
        departamento = Departamento.objects.update_or_create(codigo=local_instalacao[1], defaults={'codigo': local_instalacao[1], 'traducao': '', 'planta': planta})[0]
        area = Area.objects.update_or_create(codigo=local_instalacao[2], defaults={'codigo': local_instalacao[2], 'traducao': '', 'departamento': departamento})[0]
        linha = Linha.objects.update_or_create(codigo=local_instalacao[3], defaults={'codigo': local_instalacao[3], 'traducao': '', 'area': area})[0]
        zona = Zona.objects.update_or_create(codigo=local_instalacao[4], defaults={'codigo': local_instalacao[4], 'traducao': '', 'linha': linha})[0]
        posto = Posto.objects.update_or_create(codigo=local_instalacao[5], defaults={'codigo': local_instalacao[5], 'traducao': '', 'zona': zona})[0]
    except IndexError:
        pass

    try:
        return Equipamento.objects.update_or_create(
            codigo_sap=row['Equipamento'],
            defaults = {
                'codigo_sap': row['Equipamento'],
                'denominacao': row['Denominação'],
                'denominacao_linha': row['Denominação9'],
                'local': row['Loc.instalação'],
                'planta': planta,
                'departamento': departamento,
                'area': area,
                'linha': linha,
                'zona': zona,
                'posto': posto,
                'sala': row['Sala'],
                'equip_superior': eqp_sup,
                'codigo_abc': row['Código ABC'],
                'qrcode': '',
                'data_criacao': row['Dta.criação'],
                'data_edicao': row['Modificado em'],
                'criado_por': row['Criado por'],
                'editado_por': row['Modificado por'],
            }
        )[0]
    except Exception as e:
        print(e)
        ipdb.set_trace()


def filter_on_df(df):
    print("Filtrando equipamentos inativos") 
    inactive_equipments = []
    indexes_to_drop = []
    for key, equipment in df.iterrows():

        # Denominação
        c1 = str(equipment['Denominação']).lower().find('desat') # -1 if not, or >= 0 if room is deactivated
        c2 = str(equipment['Denominação']).lower().find('labo') # -1 if not, or >= 0 if room is deactivated
        c3 = str(equipment['Denominação']).lower().find('formação_cia') # -1 if not, or >= 0 if room is deactivated
        if c1 >= 0 or c2 >= 0 or c3 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue

        # Ordenação
        c1 = str(equipment['Campo ordenação']).lower().find('desat') # -1 if not, or >= 0 if room is deactivated
        if c1 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue

        # Nº inventário
        c1 = str(equipment['Nº inventário']).lower().find('desat') # -1 if not, or >= 0 if room is deactivated
        if c1 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue
        
        # Nº licença
        c1 = str(equipment['Nº licença']).lower().find('desat') # -1 if not, or >= 0 if room is deactivated
        if c1 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue

        # Sala
        c1 = str(equipment['Sala']).lower().find('des/des') 
        c2 = str(equipment['Sala']).lower().find('dest/des') 
        if c1 >= 0 or c2 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue
        
        # Denominação9
        c1 = str(equipment['Denominação9']).lower().find('desat') 
        c2 = str(equipment['Denominação9']).lower().find('desab') 
        c3 = str(equipment['Denominação9']).lower().find('labo') 
        if c1 >= 0 or c2 >= 0 or c3 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue
        
        # Status sistema
        c1 = str(equipment['Status sistema']).lower().find('inat') 
        if c1 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue
        
        # Local da instalação
        c1 = str(equipment['Loc.instalação']).lower().find('lab') 
        if c1 >= 0:
            indexes_to_drop.append(key)
            inactive_equipments.append(equipment)
            continue
        
    # Remove equipamentos invativos
    df.drop(df.index[indexes_to_drop], inplace=True)
    print(f"Total de equipamentos inativos {len(inactive_equipments)}")
    print(f"Criando {len(df)} equipamentos ativos")
    return df


def read_xlsx() -> pd.DataFrame:
    print("Reading xlsx file")
    return pd.read_excel(os.getcwd() + '/platecplatform/services/xlsx_importers/xlsx_db/equipamentos.xlsx', sheet_name='Planilha1'); print("Done")

def eqp_0():
    eqp_0 = Equipamento.objects.update_or_create(codigo_sap=0, defaults={
        "denominacao": "Equipamento temporário para registro de hisotrico",
        "denominacao_linha": "Equipamento temporário para registro de hisotrico",
        "local": "Equipamento temporário para registro de hisotrico",
        "codigo_abc": "1"
    })

def equipment_importer():
    raw_df = read_xlsx()
    filtered_df = filter_on_df(raw_df)
    """Create plants"""
    [Planta.objects.update_or_create(codigo=plant, defaults={'codigo': plant, 'traducao': ''}) for plant in ['VP01', 'CMO1', 'VU01'] ]
    eqp_0()
    print(f"Total de {len(raw_df)} equipamentos")
    for key, row in tqdm(filtered_df.iterrows()):
        equipments(row, df=filtered_df)
    print("Done")


if __name__ == '__main__': equipment_importer()

# from platecplatform.services.xlsx_importers.sap_equipments import equipment_importer; equipment_importer()
