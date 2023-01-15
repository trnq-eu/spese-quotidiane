import streamlit as st
from deta import Deta
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


st.title("TRACCIATORE DI SPESE 2023")

categorie = ["Spesa", "Libri", "Salute", "Ristorazione", "Intrattenimento",
            "Animali", "Scuola", "Oggetti", "Gas", "Luce", "Internet",
            "Casa", "Tecnologia", "Trasporti", "Vacanze", "Abbigliamento",
            "Regali", "Bimbi", "Tasse", "Altro"     
            ]

now = datetime.now()
current_year = now.year

# Connessione al database tramite la Project Key di Deta
deta = Deta(st.secrets["deta_key"])

# Crea il database
db = deta.Base("spese-db")

with st.form('form'):
    importo = st.number_input('Importo: ', value=0, step=10)
    categoria = st.selectbox('Categoria: ', categorie)
    descrizione = st.text_input('Descrizione: ')
    timestamp = now.strftime('%Y-%m-%d')
    submitted = st.form_submit_button('INVIA')



def data_cleaning(db_content):
#     Esempio di codice per cancellare i record che contengono la parola "prova" nella descrizione
    for entry in db_content:
        if "Prova" in entry["descrizione"]:
            db.delete(entry["key"])

def read_and_process_data():
    db_content = db.fetch().items            
    df = pd.DataFrame(db_content)

    # Converti il campo timestamp in un oggetto datatime di pandas
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filtra i record del 2023
    df_current = df[df["timestamp"].dt.year == current_year]

    # Raggruppa i dati per mese e somma le spese per ogni mese
    spese_mensili = df_current.groupby(df_current.timestamp.dt.month)['importo'].sum()

    # Raggruppa le spese per categoria
    spese_categoria = df_current.groupby("categoria")["importo"].sum()
    data_cleaning(db_content)

    return spese_mensili, spese_categoria, df_current, db_content

# Invio form
def form_submission():
    db.put({"importo": importo, "categoria": categoria, "descrizione": descrizione,
            "timestamp": timestamp})


def data_plot():    
    spese_mensili, spese_categoria, df_current, db_content = read_and_process_data()

    df_clean = df_current[df_current['descrizione'] != 'Placeholder'].sort_values(by="timestamp")
    st.write("Ultimi record: ", df_clean.tail(10))

    # Crea due subplot per poter visualizzare due grafici diversi e ovviare alla deprecazione di st.pyplot()
    fig, axs = plt.subplots(2,1)
    plt.subplots_adjust(hspace=0.5)

    # Plotta il grafico delle spese suddivise per mese
    axs[0].bar(spese_mensili.index, spese_mensili.values)
    axs[0].set_xticks(spese_mensili.index)
    axs[0].set_ylabel("Importo")
    axs[0].set_title("Spese suddivise per mese")

    # Plotta il grafico delle spese suddivise per categoria
    axs[1].barh(spese_categoria.index, spese_categoria.values)
    axs[1].set_yticks(spese_categoria.index)
    axs[1].set_ylabel("Importo")
    axs[1].set_title("Spese suddivise per categoria")

    st.pyplot(fig)

    # Creare un bottone per effettuare il download di un file csv dell'intero db
    # Crea il csv a partire dal dataframe

    df = pd.DataFrame(db_content)
    csv = df.to_csv(index=False).encode('utf-8')

    # Crea un bottone per scaricare il file csv
    st.download_button(
        "Clicca per scaricare il file csv",
        csv,
        "spese.csv",
        "text/csv",
        key='download-csv'
    )
# Cliccando il bottone, scrive un file csv all'interno del browser



if submitted:
    form_submission()
    data_plot()

if st.button("Visualizza i dati"):
    data_plot()