import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt
import streamlit as st


st.set_page_config(page_title='EV Analysis')
st.title("ELECTRIC VEHICLE ANALYSIS")
st.header("2017-2022")

# READ FILE WITH FUNCTION TO OMPTIMIZING COMPUTATION
@st.experimental_memo(ttl=60,max_entries=10)
@st.cache(suppress_st_warning=True)  # 👈 Added this

def read_masDat(): 
    return pd.read_csv("https://drive.google.com/uc?export=download&id=1FEodh3Mxo-tEG65rlQr9BNukNdvHJfEA",
                         sep=";")
evMasDat=read_masDat()

evMasDat=evMasDat.astype({"Date":"datetime64[ns]"})
evMasDat['Year']=evMasDat['Date'].dt.year
evMasDat['Month']=evMasDat['Date'].dt.month

# DESCRIBE
evDesc=evMasDat.describe()

# LIST SELECTION
listVPU=evMasDat['Vehicle Primary Use'].sort_values(ascending=True).unique().tolist()
listState=evMasDat['State'].sort_values(ascending=True).unique().tolist() ; listState.insert(0,"ALL")
listCountry=evMasDat['County'].sort_values(ascending=True).unique().tolist(); listCountry.insert(0,"ALL")

# DATA PREP
listValue=evMasDat[['Plug-In Hybrid Electric Vehicles (PHEVs)',
                   'Battery Electric Vehicles (BEVs)',
                   'Electric Vehicle (EV) Total',
                   'Total Vehicles']].columns.values.tolist()

# WIDGET
vpuSelection = st.multiselect('Vehicle Primary Use : ',
                              listVPU,
                              default=listVPU)

stateSelection = st.selectbox('State : ',
                              listState)

if stateSelection != "ALL":
    lsevMasDat=evMasDat[evMasDat['State']==stateSelection]
    listCountry=lsevMasDat['County'].sort_values(ascending=True).unique().tolist()
    countrySelection = st.selectbox('Country : ',
                                  listCountry)
else: 
    countrySelection = st.selectbox('Country : ',
                                  listCountry)

# FILTER DATAFRAME
if stateSelection == "ALL" and countrySelection == "ALL" :
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection))]

elif stateSelection != "ALL" and countrySelection == "ALL" :    
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection)) &
                     (evMasDat['State']==stateSelection)& (evMasDat['County'].notnull())]
    
elif stateSelection == "ALL" and countrySelection != "ALL" :
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection)) &
                     (evMasDat['State'].notnull())& (evMasDat['County']==countrySelection)]

elif stateSelection != "ALL" and countrySelection != "ALL" :
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection)) &
                     (evMasDat['State']==stateSelection)& (evMasDat['County']==countrySelection)]

    
    
gbVchTotal=evMasDatFil.groupby(['Year','Month'])[listValue].sum().reset_index()

#PLOTING TOTAL VEHICLE
vhcTotal=px.bar(gbVchTotal,x="Year",
               y=listValue[3],
               title="AMERICANS VEHICLE TRENDS 2017-2022",
               color="Month",
               height=500,
               text_auto=".3s")

# PLOTING TOTAL EV
vhcEVTotal=px.bar(gbVchTotal,x="Year",
               y=listValue[0:3],
               title="AMERICANS ELECTRIC VEHICLE TRENDS 2017-2022",
               height=500,
               barmode="group")

st.plotly_chart(vhcTotal)
st.plotly_chart(vhcEVTotal)

# CLEAR EXPERIMENTAL MEMOS
st.experimental_memo.clear()
