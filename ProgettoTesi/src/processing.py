import copy
import pandas as pd
import numpy as np


def column_from_dfT(csv_target): # csv_target contiene il percorso del file targ.csv
    tar = [] # lista vuota
    target_gold = []  # lista vuota
    dfT = pd.read_csv(csv_target) # dataframe risultante dalla lettura del csv
    sentences = dfT['mydeveloper_comment'].tolist()  # estrapola la colonna delle frasi
    tar_gold = dfT['Target'].tolist() # estrapola la colonna delle frasi
    target = dfT['Targets'].tolist() # estrapola la colonna dei target
    new_target = ['NA' if x is np.nan else x for x in target] # rimpiazza i valori nan float con 'NA' stringa nella lista di target
    for s in new_target:  # new_target contiene uno o più target rilevati per ogni frase
        x = s.split()  # in questo modo si suddividono i target multipli per ogni frase
        tar.append(x)  # in modo tale da inserirli nella lista tar come singoli
    for e in tar_gold:  # tar_gold bisogna pulirlo dai /
        y = str(e).replace('/', ' ')  # rimpiazza il carattere / inutile
        target_gold.append(y)  # in modo tale da inserirli nella lista target_gold come singoli
    return sentences, target_gold, tar # restituisce la lista delle frasi e la lista dei target gold e i target estratti


def column_from_dfO(csv_opinion):  # csv_target contiene il percorso del file targ.csv
    opi = [] # lista vuota
    dfO = pd.read_csv(csv_opinion)  # dataframe risultante dalla lettura del csv
    opinion = dfO['Opinions'].tolist()  # estrapola la colonna dei target
    new_opinion = ['NA' if x is np.nan else x for x in opinion]  # rimpiazza i valori nan float con 'NA' stringa nella lista di target
    for s in new_opinion:  # new_target contiene uno o più target rilevati per ogni frase
        x = s.split()  # in questo modo si suddividono i target multipli per ogni frase
        opi.append(x)  # in modo tale da inserirli nella lista tar come singoli
    return opi


# questo metodo verifica il matching tra la lista dei target estratti
# con la lista dei target gold
def lista_correct_target(lista_target_estratti, lista_target_gold):
    list_correct_target = copy.deepcopy(lista_target_estratti)  # lista che conterrà i si e no dei target corretti
    list_correct_words = copy.deepcopy(lista_target_estratti)  # lista che conterrà i termini matchati
    for i in range(0, len(lista_target_estratti)):
        for j in range(0, len(lista_target_estratti[i])):
            if str(lista_target_estratti[i][j].lower()+' ') in str(lista_target_gold[i]).lower()+' ':  # confronto dei termini nelle due liste
                a = 'si' # a è l'insieme degli elementi in comune alle due 7-uple
                list_correct_words[i][j] = lista_target_estratti[i][j]  # salvo il termine corretto
            else:
                a = 'no'
                list_correct_words[i][j] = 'NA'  # salvo NA per indicare che il termine non è corretto
            list_correct_target[i][j] = a # aggiungo alla lista i si o no per ogni termine matchato
    print(list_correct_words)
    print(list_correct_target)

    # qui conto i si scritti nella lista
    x = 0
    for i in range(0, len(list_correct_target)):
        for j in range(0, len(list_correct_target[i])):
            if list_correct_target[i][j] == 'si':
                x = x+1

    # qui prelevo la dimensione della lista dei target gold non essendo fissa a 723 perchè mancano alcuni che hanno nan
    size = 0
    for i in range(0, len(list_correct_target)):
        if str(lista_target_gold[i]) != 'nan':
            size = size+1
    # restituisce la lista con si e no, il numero di si nella lista e la lunghezza della lista gold effettiva
    return list_correct_target, x, size


