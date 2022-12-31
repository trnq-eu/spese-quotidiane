# Spese quotidiane

Un'applicazione per il tracciamento e la visualizzazione delle spese quotidiane.

L'applicazione è scritta in Python e utilizza il framework [Streamlit](https://streamlit.io/).
Il database dei record è gestito con [Deta](https://www.deta.sh/), un database NoSQL in cloud.

Altre librerie utilizzate: Pandas per la creazionde dei dataframe e Matplotlib Pyplot per i grafici.

La prima parte dell'applicazione è composta da un form che consente di inserire nuovi record. Per ogni record si può indicare l'importo, la categoria (da una lista) e una breve descrizione.
L'invio di ogni record assegna automaticamente un timestamp che viene utilizzato per raggruppare i record per mese.

Sotto al form è presente una tabella che visualizza la coda degli ultimi record inseriti per l'anno corrente.

Seguono due grafici che visualizzano le spese raggruppate per **mese** e per **categoria** *nell'anno corrente*.

