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
    for e in tar_gold:  # new_target contiene uno o più target rilevati per ogni frase
        y = str(e).replace('/', ' ')  # in questo modo si suddividono i target multipli per ogni frase
        target_gold.append(y)  # in modo tale da inserirli nella lista tar come singoli
    return sentences, target_gold, tar # restituisce la lista delle frasi e la lista dei target separati relativi alle frasi

def column_from_dfO(csv_opinion): # csv_target contiene il percorso del file targ.csv
    opi = [] # lista vuota
    dfO = pd.read_csv(csv_opinion) # dataframe risultante dalla lettura del csv
    opinion = dfO['Opinions'].tolist() # estrapola la colonna dei target
    new_opinion = ['NA' if x is np.nan else x for x in opinion] # rimpiazza i valori nan float con 'NA' stringa nella lista di target
    for s in new_opinion:  # new_target contiene uno o più target rilevati per ogni frase
        x = s.split()  # in questo modo si suddividono i target multipli per ogni frase
        opi.append(x)  # in modo tale da inserirli nella lista tar come singoli
    return opi
# questo metodo verifica il matching tra la lista dei target estratti con i 'NA'
# con la lista dei target gold con i 'NA1'
def lista_correct_target(lista_target_estratti, lista_target_gold):
    list_correct_target = copy.deepcopy(lista_target_estratti) # lista vuota che conterrà gli elementi in comune
    # metodo zip combina la x=7-upla in pos 0 di lista_target_estratti_P con la y=7-upla in pos 0 di lista_target_gold_P
    list_correct_words = copy.deepcopy(lista_target_estratti)
    for i in range(0, len(lista_target_estratti)):
        for j in range(0, len(lista_target_estratti[i])):
            if str(lista_target_estratti[i][j].lower()+' ') in str(lista_target_gold[i]).lower()+' ':
                a = 'si' # a è l'insieme degli elementi in comune alle due 7-uple
                list_correct_words[i][j] = lista_target_estratti[i][j]
            else:
                a = 'no'
                list_correct_words[i][j] = 'NA'
            list_correct_target[i][j] = a # aggiungo alla lista gli elementi in comune
    print(list_correct_words)
    print(list_correct_target)

    x = 0
    for i in range(0, len(list_correct_target)):
        for j in range(0, len(list_correct_target[i])):
            if list_correct_target[i][j] == 'si':
                x = x+1
    # restituisce la lista con si e no, il numero di si nella lista e la lunghezza della lista (ovvero numero di frasi)
    return list_correct_target, x, list_correct_target.__len__()


