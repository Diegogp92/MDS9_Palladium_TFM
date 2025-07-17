# Insctrucciones para consola cmd:
    
    # 0) Cambiar al directiorio de la app si no estamos en él.
    # cd C:\DEV\TFM\00_TFM_PALLADIUM\06_STREAMLIT

    # 1) Crear venv:
    # Ctrl + ñ # Para abrir terminal
    # py -3.12 -m venv venv # Para crear entorno virtual

    # 2) Activar el venv:
    # venv\Scripts\activate

    # 3) Instalar requerimientos de la app:
    # pip install -r requirements.txt

    # 4) Ejecutar la app en Streamlit:
    # streamlit run OptiStAI.py


# Cargamos las librerías que consideremos necesarias
import pandas as pd
import numpy as np
import pickle
import streamlit as st
import datetime
import yfinance as yf
import sklearn

st.image("Logo_Palladium.jpg", use_container_width=True)
st.header("Powered by OptiStAI")
st.subheader("Te damos la bienvenida a nuestra web de reservas. Esperamos que disfrutes de tu estancia con nosotros.")

df_dropdown = pd.read_csv(r'C:\DEV\TFM\00_TFM_PALLADIUM\06_STREAMLIT\Datos_a_extraer.csv', sep = ';')

# Inicialización a None
hotel_sel = None
llegada_sel = None
salida_sel = None
regimen_sel = None
tipo_sel = None
uso = None
adultos = None
nenes = None
bebes = None
tipo_cliente_sel = None
cliente_sel = None
grupo_sel = None
moneda_sel = None
supletoria_sel = None
cunas_sel = None
fidelidad_sel = None
comercializadora_sel = None
pais_sel = None
continente_sel = None
segmento_sel = None
fuente_sel = None
cupon = None

#df_dropdown['HOTEL'].dropna().to_list()
# HOTEL
hotel_sel = st.selectbox(
    "¿En cuál de nuestros hoteles te quieres hospedar?",
    ["-- Sin selección --"] + df_dropdown['HOTEL'].dropna().astype(str).tolist()
)
if hotel_sel == "-- Sin selección --":
    st.warning("Por favor, selecciona para continuar.")
    st.stop()
else:
    st.success(f"Correcto")
print(hotel_sel)

# FECHAS
if hotel_sel != "-- Sin selección --":
    # Llegada
    llegada_sel = st.date_input("Fecha de llegada", value=datetime.date.today())
    # Salida
    salida_sel = st.date_input("Fecha de salida", value=datetime.date.today())
    # Validación de fechas
    if (salida_sel < llegada_sel) | (llegada_sel < datetime.date.today()):
        st.error("Fechas inválidas")
        st.stop()
    else:
        st.success(f"Correcto")
        # Aquí podrías continuar con el formulario, disponibilidad, etc.
print(llegada_sel)
print(salida_sel)

# REGIMEN
if (salida_sel >= llegada_sel) & (llegada_sel > datetime.date.today()):
    regimen_sel = st.selectbox(
        "¿Qué régimen necesitas?",
        ["-- Sin selección --"] + df_dropdown['REGIMEN'].dropna().astype(str).tolist()
    )
    if regimen_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(regimen_sel)

# TIPO
if regimen_sel != "-- Sin selección --":
    tipo_sel = st.selectbox(
        "Selecciona el tipo de habitación:",
        ["-- Sin selección --"] + df_dropdown['TIPO'].dropna().astype(str).tolist()
    )
    if tipo_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(tipo_sel)

# PAX
if tipo_sel != "-- Sin selección --":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        uso = st.number_input("Uso (Invisible)", min_value=1, max_value=6, value=2, step=1)
    with col2:
        adultos = st.number_input("Adultos", min_value=0, max_value=8, value=2, step=1)
    with col3:
        nenes = st.number_input("Niños", min_value=0, max_value=6, value=0, step=1)
    with col4:
        bebes = st.number_input("Bebés", min_value=0, max_value=3, value=0, step=1)
    if adultos + nenes > 8:
        st.warning("El máximo de ocupantes por habitación es 8, sin incluir bebés")
        st.stop()
    else:
        st.success(f"Correcto")
print(adultos + nenes)

# TIPO_CLIENTE Y CLIENTE
if adultos + nenes <= 8:
    st.markdown("Selecciona tu tipo y usuario de cliente Palladium acreditado. Si no dispones de uno, por favor regístrate en: https://www.example.com")
    col1, col2 = st.columns(2)
    with col1:
        tipo_cliente_sel = st.selectbox(
        "Tipo (Prototipo)",
        ["-- Sin selección --"] + df_dropdown['TIPO_CLIENTE'].dropna().astype(int).tolist()
        )
    with col2:
        cliente_sel = st.selectbox(
        "Usuario",
        ["-- Sin selección --"] + df_dropdown['CLIENTE'].dropna().astype(str).tolist()
        )
    if (tipo_cliente_sel == "-- Sin selección --") | (cliente_sel == "-- Sin selección --"):
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(tipo_cliente_sel)
print(cliente_sel)

# GRUPO
if (tipo_cliente_sel != "-- Sin selección --") & (cliente_sel != "-- Sin selección --"):
    grupo_sel = st.selectbox(
        "¿Vuestra organización es en grupo o individual?",
        ["-- Sin selección --", "Individual", "En grupo"]
    )
    if grupo_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        if grupo_sel == "En grupo":
            grupo_sel = 1
        else:
            grupo_sel = 0
        st.success(f"Correcto")
print(grupo_sel)

# MONEDA
if grupo_sel != "-- Sin selección --":
    moneda_sel = st.selectbox(
        "Selecciona tu divisa: (Prototipo, será autodetectable)",
        ["-- Sin selección --"] + df_dropdown['MONEDA'].dropna().astype(str).tolist()
    )
    if moneda_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(moneda_sel)

# SUPLETORIA y CUNAS
if moneda_sel != "-- Sin selección --":
    st.markdown("¿Necesitas alguno de los siguientes extras?")
    col1, col2 = st.columns(2)
    with col1:
        supletoria_sel = st.number_input("Cama supletoria", min_value=0, max_value=1, value=0, step=1)
    with col2:
        cunas_sel = st.number_input("Cunas", min_value=0, max_value=3, value=0, step=1)
    st.success(f"Correcto")
print(supletoria_sel)
print(cunas_sel)

# FIDELIDAD
if moneda_sel != "-- Sin selección --":
    fidelidad_sel = st.selectbox(
        "Selecciona tu programa de fidelidad",
        ["-- Sin selección --"] + df_dropdown['FIDELIDAD'].dropna().astype(str).tolist()
    )
    if fidelidad_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(fidelidad_sel)

# COMERCIALIZADORA
if fidelidad_sel != "-- Sin selección --":
    comercializadora_sel = st.selectbox(
        "¿Eres una comercializadora regulada por Palladium?",
        ["-- Sin selección --", "Sí", "No"]
    )
    if comercializadora_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        if comercializadora_sel == "Sí":
            comercializadora_sel = 1
        else:
            comercializadora_sel = 0
        st.success(f"Correcto")
print(comercializadora_sel)

# PAÍS
if comercializadora_sel != "-- Sin selección --":
    pais_sel = st.selectbox(
        "¿Desde qué país estás realizando la reserva? (Prototipo, será autodetectable)",
        ["-- Sin selección --"] + df_dropdown['PAIS'].dropna().astype(str).tolist()
    )
    if pais_sel == "-- Sin selección --":
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(pais_sel)

# CONTINENTE
df_pais = pd.read_csv(r"C:\DEV\TFM\00_TFM_PALLADIUM\02_DATASETS_GENERADOS\paises_continentes.csv", sep=";")
continente_sel = df_pais.loc[df_pais['PAIS'] == pais_sel, 'CONTINENTE'].iloc[0]
print(continente_sel)

# SEGMENTO Y FUENTE_NEGOCIO
# Podríamos inferirlo por el segmento pero es imposible, la relación entre ellos en el dataset de reservas es n:n
if pais_sel != "-- Sin selección --":
    st.markdown("¿Cuáles son tu segmento y fuente de negocio? (Prototipo no debería seleccionarlo el cliente)")
    col1, col2 = st.columns(2)
    with col1:
        segmento_sel = st.selectbox(
        "Segmento",
        ["-- Sin selección --"] + df_dropdown['SEGMENTO'].dropna().astype(str).tolist()
        )
    with col2:
        fuente_sel = st.selectbox(
        "Fuente",
        ["-- Sin selección --"] + df_dropdown['FUENTE_NEGOCIO'].dropna().astype(str).tolist()
        )
    if (segmento_sel == "-- Sin selección --") | (fuente_sel == "-- Sin selección --"):
        st.warning("Por favor, selecciona para continuar.")
        st.stop()
    else:
        st.success(f"Correcto")
print(segmento_sel)
print(fuente_sel)

# VALOR_USD ###################################################################################################################################################

# Genero el df necesario para el pickle metamodelo de precios
df_precios = pd.DataFrame([{
    'HOTEL': hotel_sel,
    'LLEGADA_MES': llegada_sel.month,
    'LLEGADA_DIAm': llegada_sel.day,
    'LLEGADA_DIAs': llegada_sel.isoweekday(),
    'NOCHES': (salida_sel - llegada_sel).days,
    'REGIMEN': regimen_sel,
    'TIPO': tipo_sel,
    'PAX_NUM': adultos + nenes,
    'TIPO_CLIENTE': tipo_cliente_sel,
    'LT_TOMA_LLEGADA': (llegada_sel - datetime.date.today()).days,
    'FIDELIDAD': fidelidad_sel,
    'COMERCIALIZADORA': comercializadora_sel,
}])

# Ajusto sus tipos de datos
df_precios['HOTEL'] = df_precios['HOTEL'].astype('category', errors='raise')
df_precios['LLEGADA_MES'] = pd.to_numeric(df_precios['LLEGADA_MES'], errors='raise').astype('category')
df_precios['LLEGADA_DIAm'] = pd.to_numeric(df_precios['LLEGADA_DIAm'], errors='raise').astype('category')
df_precios['LLEGADA_DIAs'] = pd.to_numeric(df_precios['LLEGADA_DIAs'], errors='raise').astype('category')
df_precios['NOCHES'] = pd.to_numeric(df_precios['NOCHES'], errors='raise').astype('Int64')
df_precios['REGIMEN'] = df_precios['REGIMEN'].astype('category', errors='raise')
df_precios['TIPO'] = df_precios['TIPO'].astype('category', errors='raise')
df_precios['PAX_NUM'] = pd.to_numeric(df_precios['PAX_NUM'], errors='raise').astype('Int64')
df_precios['TIPO_CLIENTE'] = pd.to_numeric(df_precios['TIPO_CLIENTE'], errors='raise').astype('category')
df_precios['LT_TOMA_LLEGADA'] = pd.to_numeric(df_precios['LT_TOMA_LLEGADA'], errors='raise').astype('Int64')
df_precios['FIDELIDAD'] = df_precios['FIDELIDAD'].astype('category', errors='raise')
df_precios['COMERCIALIZADORA'] = pd.to_numeric(df_precios['COMERCIALIZADORA'], errors='raise').astype('category')


print(df_precios.dtypes)
print(df_precios.columns)
# Predigo el precio

with open(r"C:\DEV\TFM\00_TFM_PALLADIUM\01_MODELOS\Metamodelo_LGBM_Precios.pkl", "rb") as f:
    Metamodelo_LGBM_Precios = pickle.load(f)
valor_usd = Metamodelo_LGBM_Precios.predict(df_precios)
df_precios['VALOR_USD'] =  valor_usd

print(df_precios.head())

# Cambio de divisa
df_USD_X = pd.DataFrame()
primera_fecha = datetime.date.today() - datetime.timedelta(days=10) # Cara cubrirnos ante festivos
ultima_fecha = datetime.date.today()
df_USD_X['FECHA'] = pd.date_range(start = primera_fecha, end = ultima_fecha, freq='D')

lista_monedas = [
    'JMD', # Dolar Jamaicano
    'DOP', # Peso Dominicano
    'MXN', # Peso Mexicano
    'BRL', # Real Brasileño
]

df_USD_X['USD'] = 1

for moneda in lista_monedas:
    df_moneda = yf.download(f"{moneda}=X", start = primera_fecha, end = ultima_fecha, interval="1d")
    df_moneda = df_moneda[['Close']]
    df_moneda = df_moneda.reindex(df_USD_X['FECHA'])
    df_moneda['Close'] = df_moneda['Close'].ffill()
    df_moneda = pd.DataFrame(df_moneda.values)
    df_moneda.columns = [f"{moneda}"]
    df_USD_X = pd.concat([df_USD_X, df_moneda], axis=1)

df_USD_X = df_USD_X.tail(1) # Para quedarnos con el día de hoy
factor_multiplicador_moneda = df_USD_X[moneda_sel].iloc[0]
print(factor_multiplicador_moneda)

if (segmento_sel != "-- Sin selección --") & (fuente_sel != "-- Sin selección --"):
    cupon = st.text_input("¿Dispones de algún cupón de despuento? Si es así, introdúcelo aquí: (W95JNG9EL = GRATIS)")

if (segmento_sel != "-- Sin selección --") & (fuente_sel != "-- Sin selección --"):
    if cupon == "W95JNG9EL":
        st.metric(label="Coste Total", value=f"{0} {moneda_sel}")
    else:
        st.metric(label="Coste Total (Prototipo, basado en metamodelo. Puede haber desviaciones respecto a tarifas reales)", value=f"{(valor_usd[0]*factor_multiplicador_moneda):,.2f} {moneda_sel}")
# Continuar
    # pipeline de datos y configuración de sus tipos
    # segmentacion hoteles
    # prediccion de cancelacion

df_reservas = df_precios.copy()

# Pipeline de datos con sus tipos correctos

#df_reservas['HOTEL'] = df_reservas['HOTEL'].astype('category', errors='raise')
#df_reservas['LLEGADA_MES'] = pd.to_numeric(df_reservas['LLEGADA_MES'], errors='raise').astype('category')
#df_reservas['LLEGADA_DIAm'] = pd.to_numeric(df_reservas['LLEGADA_DIAm'], errors='raise').astype('category')
#df_reservas['LLEGADA_DIAs'] = pd.to_numeric(df_reservas['LLEGADA_DIAs'], errors='raise').astype('category')

df_reservas['LLEGADA_AVANCE'] = (llegada_sel.timetuple().tm_yday - 1)/((pd.Timestamp(year=llegada_sel.year, month=12, day=31)).timetuple().tm_yday)
df_reservas['LLEGADA_AVANCE'] = pd.to_numeric(df_reservas['LLEGADA_AVANCE'], errors='raise').astype(float)

df_reservas['SALIDA_MES'] = salida_sel.month
df_reservas['SALIDA_MES'] = pd.to_numeric(df_reservas['SALIDA_MES'], errors='raise').astype('category')

df_reservas['SALIDA_DIAm'] = salida_sel.day
df_reservas['SALIDA_DIAm'] = pd.to_numeric(df_reservas['SALIDA_DIAm'], errors='raise').astype('category')

df_reservas['SALIDA_DIAs'] = salida_sel.isoweekday()
df_reservas['SALIDA_DIAs'] = pd.to_numeric(df_reservas['SALIDA_DIAs'], errors='raise').astype('category')

df_reservas['SALIDA_AVANCE'] = (salida_sel.timetuple().tm_yday - 1)/((pd.Timestamp(year=salida_sel.year, month=12, day=31)).timetuple().tm_yday)
df_reservas['SALIDA_AVANCE'] = pd.to_numeric(df_reservas['SALIDA_AVANCE'], errors='raise').astype(float)

#df_reservas['NOCHES'] = pd.to_numeric(df_reservas['NOCHES'], errors='raise').astype('Int64')

df_reservas['DURACION_ESTANCIA'] = 'MuyLarga'
df_reservas.loc[df_reservas['NOCHES'] < 30, 'DURACION_ESTANCIA'] = 'Larga'
df_reservas.loc[df_reservas['NOCHES'] < 14, 'DURACION_ESTANCIA'] = 'Media'
df_reservas.loc[df_reservas['NOCHES'] < 7, 'DURACION_ESTANCIA'] = 'Corta'
df_reservas.loc[df_reservas['NOCHES'] < 1, 'DURACION_ESTANCIA'] = 'SinPernocta'
df_reservas['DURACION_ESTANCIA'] = df_reservas['DURACION_ESTANCIA'].astype('category', errors='raise')

#df_reservas['REGIMEN'] = df_reservas['REGIMEN'].astype('category', errors='raise')
#df_reservas['TIPO'] = df_reservas['TIPO'].astype('category', errors='raise')

df_reservas['USO'] = uso
df_reservas['USO'] = pd.to_numeric(df_reservas['USO'], errors='raise').astype('Int64')

#df_reservas['PAX_NUM'] = pd.to_numeric(df_reservas['PAX_NUM'], errors='raise').astype('Int64')

df_reservas['PAX_CAT'] = 'Single'
df_reservas.loc[df_reservas['PAX_NUM'] == 2, 'PAX_CAT'] = 'Parejas'
df_reservas.loc[df_reservas['PAX_NUM'] > 2, 'PAX_CAT'] = 'Familias'
df_reservas['PAX_CAT'] = df_reservas['PAX_CAT'].astype('category', errors='raise')

df_reservas['ADULTOS'] = adultos
df_reservas['ADULTOS'] = pd.to_numeric(df_reservas['ADULTOS'], errors='raise').astype('Int64')

df_reservas['NENES'] = nenes
df_reservas['NENES'] = pd.to_numeric(df_reservas['NENES'], errors='raise').astype('Int64')

df_reservas['BEBES'] = bebes
df_reservas['BEBES'] = pd.to_numeric(df_reservas['BEBES'], errors='raise').astype('Int64')

#df_reservas['TIPO_CLIENTE'] = pd.to_numeric(df_reservas['TIPO_CLIENTE'], errors='raise').astype('category')

df_reservas['CLIENTE'] = cliente_sel
df_reservas['CLIENTE'] = df_reservas['CLIENTE'].astype('category', errors='raise')

df_reservas['GRUPO'] = grupo_sel
df_reservas['GRUPO'] = pd.to_numeric(df_reservas['GRUPO'], errors='raise').astype('category')

df_reservas['MONEDA'] = moneda_sel
df_reservas['MONEDA'] = df_reservas['MONEDA'].astype('category', errors='raise')

df_reservas['SUPLETORIA'] = supletoria_sel
df_reservas['SUPLETORIA'] = pd.to_numeric(df_reservas['SUPLETORIA'], errors='raise').astype('Int64')

df_reservas['CUNAS'] = cunas_sel
df_reservas['CUNAS'] = pd.to_numeric(df_reservas['CUNAS'], errors='raise').astype('Int64')

df_reservas['FECHA_TOMA_MES'] = datetime.date.today().month
df_reservas['FECHA_TOMA_MES'] = pd.to_numeric(df_reservas['FECHA_TOMA_MES'], errors='raise').astype('category')

df_reservas['FECHA_TOMA_DIAm'] = datetime.date.today().day
df_reservas['FECHA_TOMA_DIAm'] = pd.to_numeric(df_reservas['FECHA_TOMA_DIAm'], errors='raise').astype('category')

df_reservas['FECHA_TOMA_DIAs'] = datetime.date.today().isoweekday()
df_reservas['FECHA_TOMA_DIAs'] = pd.to_numeric(df_reservas['FECHA_TOMA_DIAs'], errors='raise').astype('category')

df_reservas['FECHA_TOMA_AVANCE'] = (datetime.date.today().timetuple().tm_yday - 1)/((pd.Timestamp(year=datetime.date.today().year, month=12, day=31)).timetuple().tm_yday)
df_reservas['FECHA_TOMA_AVANCE'] = pd.to_numeric(df_reservas['FECHA_TOMA_AVANCE'], errors='raise').astype(float)

#df_reservas['LT_TOMA_LLEGADA'] = pd.to_numeric(df_reservas['LT_TOMA_LLEGADA'], errors='raise').astype('Int64')
#df_reservas['FIDELIDAD'] = df_reservas['FIDELIDAD'].astype('category', errors='raise')
#df_reservas['COMERCIALIZADORA'] = pd.to_numeric(df_reservas['COMERCIALIZADORA'], errors='raise').astype('category')
#df_reservas['VALOR_USD'] = pd.to_numeric(df_reservas['VALOR_USD'], errors='raise').astype(float)

df_reservas['VALOR_USD_PAX'] = df_reservas['VALOR_USD']/df_reservas['PAX_NUM']
df_reservas['VALOR_USD_PAX'] = pd.to_numeric(df_reservas['VALOR_USD_PAX'], errors='raise').astype(float)

df_reservas['VALOR_USD_NOCHE'] = df_reservas['VALOR_USD']/df_reservas['NOCHES']
df_reservas['VALOR_USD_NOCHE'] = pd.to_numeric(df_reservas['VALOR_USD_NOCHE'], errors='raise').astype(float)

df_reservas['VALOR_USD_PAX_NOCHE'] = df_reservas['VALOR_USD']/df_reservas['PAX_NUM']/df_reservas['NOCHES']
df_reservas['VALOR_USD_PAX_NOCHE'] = pd.to_numeric(df_reservas['VALOR_USD_PAX_NOCHE'], errors='raise').astype(float)

if cupon == 'W95JNG9EL':
    df_reservas['GRATIS'] = 1
else:
    df_reservas['GRATIS'] = 0
df_reservas['GRATIS'] = pd.to_numeric(df_reservas['GRATIS'], errors='raise').astype('category')

df_reservas['PAIS'] = pais_sel
df_reservas['PAIS'] = df_reservas['PAIS'].astype('category', errors='raise')

df_reservas['CONTINENTE'] = continente_sel
df_reservas['CONTINENTE'] = df_reservas['CONTINENTE'].astype('category', errors='raise')

df_reservas['SEGMENTO'] = segmento_sel
df_reservas['SEGMENTO'] = df_reservas['SEGMENTO'].astype('category', errors='raise')

df_reservas['FUENTE_NEGOCIO'] = fuente_sel
df_reservas['FUENTE_NEGOCIO'] = df_reservas['FUENTE_NEGOCIO'].astype('category', errors='raise')

#df_reservas['CANCELADA'] = df_reservas['CANCELADA'].astype("category") <- La generaré con la predicción

#df_reservas['TAMANO_HOTEL'] = df_reservas['TAMANO_HOTEL'].astype('category', errors='raise') <- A mano con ifs

print(df_reservas.info())
print(df_reservas)

# Reordeno las columnas para que sean coherentes con los entrenamientos de los pickles

df_reservas = df_reservas[[
    'HOTEL',
    'LLEGADA_MES',
    'LLEGADA_DIAm',
    'LLEGADA_DIAs',
    'LLEGADA_AVANCE',
    'SALIDA_MES',
    'SALIDA_DIAm',
    'SALIDA_DIAs',
    'SALIDA_AVANCE',
    'NOCHES',
    'DURACION_ESTANCIA',
    'REGIMEN',
    'TIPO',
    'USO',
    'PAX_NUM',
    'PAX_CAT',
    'ADULTOS',
    'NENES',
    'BEBES',
    'TIPO_CLIENTE',
    'CLIENTE',
    'GRUPO',
    'MONEDA',
    'SUPLETORIA',
    'CUNAS',
    'FECHA_TOMA_MES',
    'FECHA_TOMA_DIAm',
    'FECHA_TOMA_DIAs',
    'FECHA_TOMA_AVANCE',
    'LT_TOMA_LLEGADA',
    'FIDELIDAD',
    'COMERCIALIZADORA',
    'VALOR_USD',
    'VALOR_USD_PAX',
    'VALOR_USD_NOCHE',
    'VALOR_USD_PAX_NOCHE',
    'GRATIS',
    'PAIS',
    'CONTINENTE',
    'SEGMENTO',
    'FUENTE_NEGOCIO',
]]

# Cargo los pickles

with open(r"C:\DEV\TFM\00_TFM_PALLADIUM\01_MODELOS\modelo_lgbm_Grande.pkl", "rb") as f:
    modelo_lgbm_Grande = pickle.load(f)
with open(r"C:\DEV\TFM\00_TFM_PALLADIUM\01_MODELOS\modelo_lgbm_Mediano.pkl", "rb") as f:
    modelo_lgbm_Mediano = pickle.load(f)
with open(r"C:\DEV\TFM\00_TFM_PALLADIUM\01_MODELOS\modelo_lgbm_Pequeno.pkl", "rb") as f:
    modelo_lgbm_Pequeno = pickle.load(f)

# Predigo con ellos

if df_reservas['HOTEL'].iloc[0] in ['ComplejoPuntaCana', 'ComplejoCostaMujeres', 'ComplejoRivieraMaya']: # Hoteles Grandes
    cancelada_pred = modelo_lgbm_Grande.predict(df_reservas)
    cancelada_proba = modelo_lgbm_Grande.predict_proba(df_reservas)

elif df_reservas['HOTEL'].iloc[0] in ['GrandPalladiumJamaica&LadyHamiltonResort', 'GrandPalladiumImbassaiResort&Spa', 'PalladiumVallarta']: # Hoteles Medianos
    cancelada_pred = modelo_lgbm_Mediano.predict(df_reservas)
    cancelada_proba = modelo_lgbm_Mediano.predict_proba(df_reservas)

else: # Hoteles Pequeños
    cancelada_pred = modelo_lgbm_Pequeno.predict(df_reservas)
    cancelada_proba = modelo_lgbm_Pequeno.predict_proba(df_reservas)

st.metric(label="Predicción de cancelación, 1 = Cancelada. (Invisible)", value=f"{cancelada_pred[0]}")
st.metric(label="La probabilidad de cancelación es: (Invisible)", value=f"{cancelada_proba[0][1]:.2%}")