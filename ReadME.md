## PROBLEMI 

1. Controllare quali llm sono compatibili con Autogen, che è il pacchetto che viene utilizzato per far comunicare gli agenti (video per autogen e scaricare modelli llm -> https://www.youtube.com/watch?v=aYieKkR_x44)

2. Problema di Edoardo -> pacchetti nvidia, non compatibili per il suo pc che è MAC. Far girare su Orfeo, ma non è possibile utilizzare LM per scaricare llm)

3. Semantic API key -> capire accessi ed endpoint, e se è gratuita nel caso in cui dimostra di far parte di un'università. Alternativa da provare a Semantic API key potrebbe essere Wikipedia API. L'intento è fargli generare le battute in base a GraphReasoning (fatto da MIT lamm) su campi scientifici.

4. Cambiare utils.py da generatore pdf a qualcosa come una chat, oppure una stanza 2D stile videogioco in cui gli agenti comunicano? -----> In generale, capire come far interagire un utente con questo progetto al fine che esso riesca a generare battute.

 
5. Redesign degli agenti: ruoli, cosa fanno.

6. Redesign dei prompt


## 7 GIUGNO 2024

# VIRTUAL ENV and how to use it

To install and activate the venv, run:

chmod +x runme.sh && source ./runme.sh

This will create and activate a virtual environment with these packages: pybind11, pandas, scipy, matplotlib, numpy

You can find the list in the file requirements.txt.
Source will keep the venv activated after running the bash script.

