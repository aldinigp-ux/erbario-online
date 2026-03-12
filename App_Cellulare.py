import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("🌿 Erbario Online di Haldin")

# Connessione
conn = st.connection("gsheets", type=GSheetsConnection)

# Lettura (Questa funziona sempre!)
df = conn.read()
lista_alberi = df['nome'].tolist()

scelta = st.selectbox("Seleziona una pianta:", ["Scegli..."] + lista_alberi)

if scelta != "Scegli...":
    dati_albero = df[df['nome'] == scelta].iloc[0]
    st.header(scelta)
    st.metric("Altezza", dati_albero['altezza'])
    
    nota_attuale = dati_albero['nota']
    nuova_nota = st.text_area("Modifica la nota:", value=nota_attuale)
    
    if st.button("Salva nota su Google Sheets"):
        # Tentativo di aggiornamento
        idx = df.index[df['nome'] == scelta].tolist()[0]
        df.at[idx, 'nota'] = nuova_nota
        
        try:
            # PROVA A SCRIVERE
            conn.update(data=df)
            st.success("Nota salvata!")
            st.balloons()
        except Exception as e:
            st.error("Google blocca la scrittura pubblica.")
            st.info("Paolo, per scrivere serve una 'Chiave Privata' (Service Account).")
            st.write("Vuoi che proviamo a crearla o preferisci usare l'app solo per consultazione dal cellulare?")