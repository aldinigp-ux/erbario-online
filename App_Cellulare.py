import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Titolo dell'App
st.title("🌿 Erbario Online di Haldin")

# 1. Connessione al foglio Google (Database Online)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Lettura dei dati
df = conn.read()

# 3. Creazione della lista dei nomi degli alberi
lista_alberi = df['nome'].tolist()

# 4. Menu a tendina per la scelta
scelta = st.selectbox("Seleziona una pianta:", ["Scegli..."] + lista_alberi)

if scelta != "Scegli...":
    # Recuperiamo la riga corrispondente alla scelta effettuata
    dati_albero = df[df['nome'] == scelta].iloc[0]
    
    st.header(scelta)
    st.write(f"**Tipo:** {dati_albero['tipo']}")
    st.metric("Altezza", dati_albero['altezza'])
    
    # Visualizzazione Foto (se c'è un link nel foglio Google)
    if str(dati_albero['foto']).startswith("http"):
        st.image(dati_albero['foto'], caption=scelta)
    
    # Area per le note
    nota_attuale = dati_albero['nota']
    nuova_nota = st.text_area("Modifica la nota:", value=nota_attuale)
    
   # Tasto per salvare le modifiche
    if st.button("Salva nota su Google Sheets"):
        try:
            # Troviamo l'indice della riga da aggiornare
            idx = df.index[df['nome'] == scelta].tolist()[0]
            df.at[idx, 'nota'] = nuova_nota
            
            # Aggiorniamo il database online
            conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=df)
            st.success("Nota salvata con successo!")
            st.balloons() # Un po' di festa per il successo!
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")
            st.info("Verifica di aver impostato il foglio Google come 'Editor' per chiunque abbia il link.")