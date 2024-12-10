import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import *

st.markdown('''
### Grupo 2
## Wide World Importers Sales Analysis
            ''')

dataframe2['Total Including Tax'] = dataframe2['Total Including Tax'].astype('float')

suma_ventas =dataframe2.groupby('Employee')['Total Including Tax'].sum().reset_index(name='Total Sales').sort_values(by='Total Sales' ,ascending=False).round(2)


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label='Total Sales',
        value= f"${dataframe2['Total Including Tax'].sum():,.2f}" 
    )

with col2:
    st.metric(
    label='Average sales',
    value= f"${dataframe2['Total Including Tax'].mean():,.2f}"  
    )

with col3:
    st.metric(
    label='Customer Count',
    value= (dataframe2['Customer Key'].count())
    )

rango_cantidad = st.slider(
      "Quantity Range",
      min_value=int(dataframe2['Quantity'].min()),
      max_value=int(dataframe2['Quantity'].max()),
      value=(int(dataframe2['Quantity'].min()),int(dataframe2['Quantity'].max()))
)

col1, col2= st.columns(2)
with col1:
    empleado = st.multiselect(
        'Employee',
        list(set(dataframe2["Employee"])),
    default=None
    )



if suma_ventas['Employee'].isin(empleado).any():
    # Hay al menos una coincidencia
    mask = suma_ventas['Employee'].isin(empleado)
    filtro_employee = suma_ventas[mask]
else:
    # No hay coincidencias
    filtro_employee = suma_ventas



with col2:
        st.multiselect(
        'State',
        list(set(dataframe2["State Province"])),
    default=None
    )

fig = px.bar(
      suma_ventas,
      x='Total Sales',
      y='Employee',
      orientation='h'
)

st.plotly_chart(fig)
