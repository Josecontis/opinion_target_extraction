import csv
import pandas as pd
import re
import numpy as np
from operator import itemgetter


# metodo per estrapolare le colonne da un file csv
def trasforma_csv_in_df_colonne_to_list(file_csv):
    dfP = pd.read_csv(file_csv) # lettura file csv delle polarità
    sentence = dfP['Sentence'].tolist() # sentence contiene una lista di frasi estrapolate
    target_polarity = dfP['Target-Polarity'].tolist() # target_polarity contiene una lista di target con polarità estrapolate
    # per ogni elemento della lista di target con polarità vengono rimpiazzati i valori nan con 'NA1'
    new_target_polarity = ['NA1' if x is np.nan else x for x in target_polarity]
    return sentence, new_target_polarity # restituisce la lista di frasi e la lista di target con polarità di ogni frase

# in input la lista dei target con le polarità unite estratte dal csv gold
def process_list_target_polarity(target_polarity):
    list_target_polarity = [] # lista vuota che conterrà i target con le polarità separate
    for str in target_polarity: # itero sulla lista dei target con le polarità [es. str='buono[+3] bello[+2]']
        x = str.split() # divide la lista di polarità in base agli spazi [es. x='buono[+3]', 'bello[+2]']
        list_tmp = [] # lista vuota temporanea
        for j in x: # per ogni termine-polarità nella lista x
            y = j.split('[') # suddivide target da polarità [es. y='buono', '+3]']
            list_tmp.append(y) # concatena alla lista temporanea y [es. list_tmp=('buono', '+3]'),('bello','+2]')... ]
        list_target_polarity.append(list_tmp)
    return list_target_polarity # restuisce la lista dei target con le polarità separate

# in input la lista dei target con le polarità separate
def listaTarget_from_listaTargetPolarity(list_target_polarity):
    lista_target = [] # lista vuota che conterrà i target
    for k in list_target_polarity: # itero su [es. list_target_polarity=('buono', '+3]'),('bello','+2]')... ]
        lista_target_tmp = [] # creo lista temporanea per contenere i target di una singola frase
        for ind in k: # itero su [es. considero K=('buono', '+3]') in ind 0]
            a = itemgetter(0)(ind) # a contiene la parola di opinione di una singola coppia k [es. a=buono]
            lista_target_tmp.append(a) # lista_target_tmp conterrà tutti i target di UNA frase
        lista_target.append(lista_target_tmp) # lista_target_tmp conterrà tutti i target di TUTTE le frasi
    return lista_target # restuisce solo la lista dei target di tutte le frasi


# in input la lista dei target con le polarità separate
def listaPolarity_from_listaTargetPolarity(list_target_polarity):
    lista_polarity = [] # lista vuota che conterrà le polarità
    for kk in list_target_polarity: # itero su [es. list_target_polarity=('buono', '+3]'),('bello','+2]')... ]
        lista_polarity_tmp = [] # creo lista temporanea per contenere le polarità di una singola frase
        for ind1 in kk: # itero su [es. considero KK=('buono', '+3]') in ind1 0]
            index = 1 # -no sense-------?????
            if len(ind1) > index: # controllo sulla lunghezza del termine target che se > 1 allora mi salvo la polarità
                b = itemgetter(1)(ind1) # salva in b la polarità in posizione ind1
                lista_polarity_tmp.append(b) # concateno alla lista
            else: # in questo caso significa che non c'è la polarità
                lista_polarity_tmp.append('NA1') # quindi nella lista inserisco 'NA1'
        lista_polarity.append(lista_polarity_tmp) # la lista delle polarità di tutte le frasi

    # procedimento per eliminare le parentesi
    lista_polarity_process = []
    for jj in lista_polarity: # per ogni polarità [es. lista_polarity=(+3]),(+2])..]
        lista_polarity_process_tmp = []
        for jjj in jj: # per ogni polarità
            if (jjj.__contains__(']')): # se contiene la parentesi ]
                x = jjj.replace("]", "") # elimino la parentesi ]
                lista_polarity_process_tmp.append(x) # inserisco nella lista temporanea il risultato [es. +3,+2...]
            else: # altrimenti significa che è già nella forma giusta da poterlo inserire nella lista
                lista_polarity_process_tmp.append(jjj)
        lista_polarity_process.append(lista_polarity_process_tmp) # inserisco la lista di polarità corrette di UNA frase nella lista finale
    return lista_polarity_process # restituisco la lista delle polarità di TUTTE le frasi


# prende la lista dei target con SOLO le polarità
def process_list_polarity_gold(lista_polarity_gold):
    l = [] # lista vuota che conterrà tutti i positivi
    for i in lista_polarity_gold: # itero sui valori numerici di tutte le frasi
        l1 = [] # lista vuota che conterrà i positivi di una frase
        for j in i: # itero sui valori numerici di una frase
            z = re.sub(r'[+]\d', "positive", j) # espressione regolare per sostituire il valore +3 con positive
            l1.append(z) # aggiungo la stringa 'positive' di UNA frase alla lista
        l.append(l1) # aggiungo le stringhe 'positive' di TUTTE le frasi alla lista

    l2 = [] # lista vuota che conterrà tutti i negativi
    for k in l: # itero sulla lista dove sono stati cambiati i numeri positivi in stringhe ma NON i numeri negativi
        l3 = [] # lista vuota che conterrà i positivi di una frase
        for y in k: # itero sui valori numerici di una frase
            w = re.sub(r'[-]\d', 'negative', y) # espressione regolare per sostituire il valore -3 con negative (\d è per i numeri, r è per rimpiazza)
            l3.append(w) # aggiungo la stringa 'negative' di UNA frase alla lista
        l2.append(l3) # aggiungo le stringhe 'negative' di TUTTE le frasi alla lista
    return l2 # la lista delle polarità sottoforma di stringhe di tutte le frasi

# ------------------- OPERAZIONI PER CREARE GOLD.CSV A PARTIRE DEL DATASET NIKON COOLPIX 4300 --------------------
# ------ non utilizzato nel main -----
def rimpiazza_caratteri_inutili(file_Originale):
    # Read in the file
    with open(file_Originale, 'r') as file: # apre il file originale in lettura
        filedata = file.read() # salva il contenuto in filedata

    # rimpiazza i diversi caratteri, non utili in fileadta
    filedata = filedata.replace('?', '.')
    filedata = filedata.replace('!', '.')
    filedata = filedata.replace(';', '')
    filedata = filedata.replace(',', '')
    filedata = filedata.replace(':', '.')
    filedata = filedata.replace('"', '')

    # scrive il file precedente in un altro privato dei caratteri rimpiazzati
    with open('../processing_fileOriginale/Nikon coolpix 4300-Copia.txt', 'w') as file:
        file.write(filedata)


# ------ non utilizzato nel main -----
def rimozione_titoli_t(file_originale_caratteri_rimpiazzati):
    # rimuove le righe dal file che rappresenano i titoli denominati con [t]
    file1 = open(file_originale_caratteri_rimpiazzati) # apre file da modificare
    file2 = open('../processing_fileOriginale/Nikon coolpix 4300.Copia2.txt', 'w') # crea nuovo file per l'output

    for line in file1.readlines(): # per ogni riga del file da modificare
        if not (line.startswith('[t]')): # se la linea non inizia con '[t]'
            file2.write(line) # scrive la linea nel file di output
    file2.close() # chiude file di output
    file1.close() # chiude file di input


# ------ non utilizzato nel main -----
def trasforma_in_csv(file_originale_processato):
    with open(file_originale_processato, 'r') as in_file: # apertura del file come lettura
        stripped = (line.strip() for line in in_file) # per ogni linea nel txt suddivide i termini in base agli spazi
        lines = (line.split("##") for line in stripped if line) # separa le frasi in base a '##'
        with open('../csv/Gold.csv', 'w') as out_file: # apertura in scrittura del file csv delle polarità
            writer = csv.writer(out_file) # crea l'oggetto writer
            writer.writerow(('Target-Polarity', 'Sentence')) # scrive la prima riga (nomi di colonne)
            writer.writerows(lines) # scrive le altre righe ricavate dal txt


# ------ non utilizzato nel main -----
# metodo che scrive le frasi in un .txt da un .csv
def scrivere_sentence_file(file, file_csv):
    sentence, target_polarity = trasforma_csv_in_df_colonne_to_list(file_csv) # estrapola colonna frasi e target con le polarità
    with open(file, 'w') as f: # con il file .txt aperto in scrittura
        for item in sentence: # itera sulle frasi
            f.write("%s\n" % item) # scrive nel file .txt la frase


# ------ non utilizzato nel main -----
def process_file(file_originale_processato):
    with open(file_originale_processato) as f:
        with open(file_prova, 'w') as f1:
            for line in f:
                f1.write(re.sub(r'([]])([a-z])', r'\1 \2', line))


file_Originale = '../processing_fileOriginale/Nikon coolpix 4300.txt'
file_originale_caratteri_rimpiazzati = '../processing_fileOriginale/Nikon coolpix 4300-Copia.txt'
file_originale_processato = '../processing_fileOriginale/Nikon coolpix 4300.Copia2.txt'
file_originale_processato_csv = '../csv/Gold.csv'
input = 'input.txt'
file_prova = '../processing_fileOriginale/Nikon coolpix 4300.Copia2 - Copia.txt'


rimpiazza_caratteri_inutili(file_Originale)
rimozione_titoli_t(file_originale_caratteri_rimpiazzati)
process_file(file_originale_processato)
trasforma_in_csv(file_prova)
trasforma_csv_in_df_colonne_to_list(file_originale_processato_csv)
scrivere_sentence_file(input, file_originale_processato_csv)

