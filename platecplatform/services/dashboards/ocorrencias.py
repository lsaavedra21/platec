import requests
import streamlit as st
import pandas as pd
import datetime

df = pd.DataFrame(requests.get(f'http://0.0.0.0:8000/api/v1/ocorrencias/').json())

today = datetime.datetime.now().date()
df['horario_quebra'] = pd.to_datetime(df['horario_quebra'])

# Filtrar as ocorrências do ano atual (2023)
current_year_occurrences = df[df['horario_quebra'].dt.year == 2023]

# Filtrar as ocorrências do ano anterior (2022)
previous_year_occurrences = df[df['horario_quebra'].dt.year == 2022]

previous_day = datetime.date.today() - datetime.timedelta(days=1)
previous_day_occurrences = df[df['horario_quebra'].dt.date == previous_day]

# Filter by previous day
previous_day = datetime.datetime.now() - datetime.timedelta(days=1)
previous_day_occurrences = df[df['horario_quebra'].dt.date == previous_day.date()]

# Filter by current week
current_week_start = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
current_week_occurrences = df[(df['horario_quebra'].dt.date >= current_week_start.date()) & (df['horario_quebra'].dt.date <= datetime.datetime.now().date())]

# Filter by current month
current_month_start = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 1)
current_month_occurrences = df[(df['horario_quebra'].dt.date >= current_month_start) & (df['horario_quebra'].dt.date <= datetime.datetime.now().date())]

# Display counts in sidebar
st.sidebar.write(f"Ocorrência Diária: {len(previous_day_occurrences)}")
st.sidebar.write(f"Ocorrência Semanal: {len(current_week_occurrences)}")
st.sidebar.write(f"Ocorrência Mensal: {len(current_month_occurrences)}")
st.sidebar.write(f"Ocorrências Ano (2022): {len(previous_year_occurrences)}")
st.sidebar.write(f"Ocorrências Ano (2023): {len(current_year_occurrences)}")

# Adicionar o buscador de ocorrências
search_options = ['Semana', 'Dia']
search_option = st.sidebar.selectbox("Buscar por", search_options)

if search_option == 'Semana':
    selected_year = st.sidebar.selectbox("Selecione o ano", [2022, 2023])
    selected_week_start = st.sidebar.selectbox("Selecione a semana inicial", list(range(1, 53)), index=0)
    selected_week_end = st.sidebar.selectbox("Selecione a semana final", list(range(1, 53)), index=51)
    occurrences = df[
        (df['horario_quebra'].dt.year == selected_year) &
        (df['horario_quebra'].dt.week >= selected_week_start) &
        (df['horario_quebra'].dt.week <= selected_week_end)
    ]
    st.sidebar.write(f"Total de ocorrências: {len(occurrences)}")

elif search_option == 'Dia':
    selected_day = st.sidebar.date_input("Selecione o dia", today)
    occurrences = df[df['horario_quebra'].dt.date == selected_day]
    formatted_date = selected_day.strftime("%d/%m/%Y")
    st.sidebar.write(f"Total de ocorrências: {len(occurrences)}")
    st.write(f"Ocorrências do dia {formatted_date}:")

def generate_ocurrence_str(row):
    eqp_dict = row.equipamento

    planta_obj = eqp_dict.get('planta')
    if planta_obj:
        planta = planta_obj.get('codigo')
    else:
        planta = "N/A"

    departamento_obj = eqp_dict.get('departamento')
    if departamento_obj:
        departamento = departamento_obj.get('codigo')
    else:
        departamento = 'N/A'

    area_obj = eqp_dict.get('area')
    if area_obj:
        area = area_obj.get('codigo')
    else:
        area = 'N/A'

    try:
        hora_pane = row.horario_quebra[11:16]
    except:
        hora_pane = 'N/A'

    try:
        hora_chamado = row.horario_chamado[11:16]
    except:
        hora_chamado = 'N/A'

    tempo_parado = row.tempo_eqp_parado

    perdas = row.veiculos_perdidos

    sintoma = row.sintoma

    causa = row.causa

    reparo = row.remedio

    res = f"""
    **Planta**: {planta} **Departamento**: {departamento} **Area**: {area} **Equipamento**: {eqp_dict['denominacao']} <br> 
    **Data/Hora da pane**: {data_quebra}, {hora_pane}     **Cham**:  {hora_chamado}  **Tempo de Eq. Parado**: {tempo_parado} **Perdas:** {perdas} <br> 
    **Sintoma**: {sintoma} <br>
    **Causa**: {causa} <br>
    **Reparo:** {reparo}
    <br>
    """
    return res


ocurrences = []
# Generate datas
data_quebra_one_day_minus = ""
turno = ""
for row in df.iterrows():
    ### OCORRÊNCIAS
    row = row[1]
    plantas = {
        '1': 'VP01',
        '2': 'CMO1',
        '3': 'VU01'
    }
    # Date treatment
    date_str = row['horario_quebra']
    date_obj = datetime.datetime.strptime(row['horario_quebra'].strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S')
    data_quebra = date_obj.strftime('%d/%m/%Y')

    if data_quebra_one_day_minus != data_quebra:
        ocurrences.append(f"### DATA {data_quebra}")
        data_quebra_one_day_minus = data_quebra
        turno = ""

    if turno != row.turno:
        turno = f'#### {row.turno}'
        ocurrences.append(turno)
        turno = row.turno

    ocurrence_str = generate_ocurrence_str(row)
    ocurrences.append(ocurrence_str)
    data_quebra_one_day_minus = data_quebra

for item in ocurrences: st.markdown(item, unsafe_allow_html=True)
