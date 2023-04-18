#import
import streamlit as st
import pandas as pd
import pydeck as pdk

#settings and vars
DATA_URL = "https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv"

#functions
@st.cache_data
def load_data():
    """Load data in cache and return df"""
    
    #rename columns
    renamed_columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    #load data
    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')

    #rename
    data = data.rename(columns=renamed_columns)

    #apply datetime to date
    data['data'] = data['data'] + ' ' + data['ocorrencia_horario']
    data['data'] = pd.to_datetime(data['data'])

    #return only renamed columns
    return data[list(renamed_columns.values())]

#load data
df = load_data()
#get classes
clfs = df['classificacao'].unique().tolist()

#SIDEBAR
# Parameters and ocurrences registries
sb = st.sidebar                 # instanciate sidebar
sb.header('Parameters')         # title
info_sb = sb.empty()            # placeholder, to display # occur

# Slidebar select year
sb.subheader('Year')            # title
filter_year = sb.slider('Select the year',min(df['data'].dt.year), max(df['data'].dt.year))

# Checkbox to show data
sb.subheader('Dataset')                     # title
show_dataset = sb.checkbox('Show dataset')  # checkbox

# multiselect classifs
filter_clf = sb.multiselect('Select the classification of occurences',
               options = clfs,
               default=['INCIDENTE','ACIDENTE'])

# slider lat
sb.subheader('Latitude')
col1, col2 = sb.columns(2)
lat_min = col1.number_input('Min',min_value=min(df['latitude']), max_value=max(df['latitude']) ,value = min(df['latitude']),step=1.0)
lat_max = col2.number_input('Max',min_value=min(df['latitude']), max_value=max(df['latitude']) ,value = max(df['latitude']),step=1.0)
lat_min, lat_max = sb.slider('hideit', min(df['latitude']), max(df['latitude']), value = (lat_min, lat_max), label_visibility='hidden')

# slider lon
sb.subheader('Longitude')
col1, col2 = sb.columns(2)
lon_min = col1.number_input('Min',min_value=min(df['longitude']), max_value=max(df['longitude']) ,value = min(df['longitude']),step=1.0)
lon_max = col2.number_input('Max',min_value=min(df['longitude']), max_value=max(df['longitude']) ,value = max(df['longitude']),step=1.0)
lon_min, lon_max = sb.slider('hideit', min(df['longitude']), max(df['longitude']), value = (lon_min, lon_max), label_visibility='hidden')


# footer note
sb.markdown("""
The database of aeronautic occurences is managed by ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")

# filter data
df_filtered = df[
    (df['data'].dt.year==filter_year) &         # year
    (df['classificacao'].isin(filter_clf)) &    # classes
    #lat and long
    ((lat_min<=df['latitude']) & (df['latitude']<=lat_max)) & ((lon_min<=df['longitude']) & (df['longitude']<=lon_max))
]

# fill info placeholder
info_sb.info(f'{len(df_filtered)} occurences selected')

#MAIN
#title
st.title('CENIPA - Aeronautic Accidents')
st.markdown(f"""(ℹ️) It's been shown occurences classified as **{', '.join(filter_clf)}** for year {filter_year}""")

#show dataset if checked
if show_dataset:
    st.write(df_filtered)
    st.download_button(label="Download data as CSV",
                       data=df_filtered.to_csv(encoding='utf-8-sig'),
                       file_name='extract.csv',
                       mime='text/csv'
                       )

#show map
st.subheader('Map occurences')
st.map(df_filtered)



