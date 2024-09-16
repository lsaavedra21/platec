from equipamentos.models import Equipamento, QuebraEquipamento
from tqdm import tqdm
import os, ipdb
import pandas as pd
import math


# Esse xlsx importer foi feito para importar as ocorrencias platec do excell, que vieram do OneNote

def verify_nan(value):
    try:
        if math.isnan(value):
            return None
    except Exception as e:
        return value
    return value

def hora_da_pane_treatment(value):
    hora = verify_nan(value)
    if hora is None: return None
    if isinstance(hora, str): return None
    if isinstance(hora, float): return None
    return hora

def ocurrences(row, eqp_0):
    horario_quebra = hora_da_pane_treatment(row['Hora da Pane'])
    # First verifications
    data = verify_nan(row['Data'])
    sintoma = verify_nan(row['Sintoma'])
    causa = verify_nan(row['Causa'])
    causa_raiz = verify_nan(row['Causa Raíz'])
    categoria = 'Outro'
    turno = verify_nan(row['Id_Turno'])
    horario_chamado = verify_nan(row['Hora Inicio do chamado'])
    tempo_eqp_parado = verify_nan(row['T. Equip. Parado'])
    veiculos_perdidos = verify_nan(row['Veic. Perdidos'])
    marcha_degradada = ''
    mbr = verify_nan(row['MBR'])

    # Start treatment
    if turno: 
        if turno.startswith('1'):
            turno = "1 Turno"
        elif turno.startswith('2'):
            turno = "2 Turno"


    if isinstance(horario_chamado, str) or isinstance(horario_chamado, float):
        horario_chamado = None
    try:
        if horario_quebra: horario_quebra = f"{data.year}-{str(data.month)}-{str(data.day)} {horario_quebra.strftime('%H:%M:%S')}"
        if horario_chamado: horario_chamado = f"{data.year}-{str(data.month)}-{str(data.day)} {horario_chamado.strftime('%H:%M:%S')}"
    except Exception as e:
        print(f"Error: {e}")
        ipdb.set_trace()
        

    if horario_quebra is None and horario_chamado: horario_quebra = horario_chamado

    if horario_quebra is None and horario_chamado is None:
        horario_quebra = data
        horario_chamado = data
    
    try:
        tempo_eqp_parado = int(tempo_eqp_parado)
    except TypeError:
        tempo_eqp_parado = 0
    except ValueError:
        tempo_eqp_parado = 0
    res = {}


    try:
        if isinstance(veiculos_perdidos, int):
            veiculos_perdidos = veiculos_perdidos
    except Exception as e:
        print(e)
        ipdb.set_trace()

    try:
        if isinstance(veiculos_perdidos, str):
            try:
                veiculos_perdidos = int("".join([str(s) for s in veiculos_perdidos if s.isdigit()])) if veiculos_perdidos else 0
            except ValueError:
                veiculos_perdidos = 0

    except Exception as e:
        print(e)
        ipdb.set_trace()


    try:
        res = {
            'equipment_id':         eqp_0,
            'sintoma':              sintoma,
            'causa':                f'Causa: {causa} - Causa Raíz: {causa_raiz}',
            'remedio':              row['Remédio'],
            'categoria':            'Outro',
            'turno':                turno,
            'horario_quebra':       horario_quebra,
            'horario_chamado':      horario_chamado,
            'tempo_eqp_parado':     tempo_eqp_parado,
            'veiculos_perdidos':    veiculos_perdidos,
            'marcha_degradada':     '',
            'mbr':                  mbr,
            }
    except Exception as e:
        print(f"Error: {e}")
        ipdb.set_trace()

    print(row)
    print("------------------------------")
    for key, value in res.items():
        print(f'{key}: {value}')

    try:
        QuebraEquipamento.objects.update_or_create(
            sintoma= sintoma,
            defaults = {**res}
        )
        print("Done")

    except Exception as e:
        print(e)
        ipdb.set_trace()



def read_xlsx() -> pd.DataFrame:
    print("Reading xlsx file")
    return pd.read_excel(os.getcwd() + '/services/xlsx_db/ocurrences/ocurrences.xlsm', sheet_name='2022'); print("Done")

def ocurrences_importer():
    eqp_0 = Equipamento.objects.get(codigo_sap=0)
    raw_df = read_xlsx()

    print(f"Total de {len(raw_df)} ocorrencias")
    for key, row in tqdm(raw_df.iterrows()):
        ocurrences(row=row, eqp_0=eqp_0)
    print("Done")


if __name__ == '__main__': ocurrences_importer()

