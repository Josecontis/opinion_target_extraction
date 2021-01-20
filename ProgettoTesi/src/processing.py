import csv
import pandas as pd
import numpy as np


def column_from_dfT(csv_target): # csv_target contiene il percorso del file targ.csv
    tar = [] # lista vuota
    dfT = pd.read_csv(csv_target) # dataframe risultante dalla lettura del csv
    sent = dfT['Sentence'].tolist() # estrapola la colonna delle frasi
    target = dfT['Target'].tolist() # estrapola la colonna dei target
    new_target = ['NA' if x is np.nan else x for x in target] # rimpiazza i valori nan float con 'NA' stringa nella lista di target
    for str in new_target: # new_target contiene uno o più target rilevati per ogni frase
        x = str.split() # in questo modo si suddividono i target multipli per ogni frase
        # print(x)
        tar.append(x) # in modo tale da inserirli nella lista tar come singoli
    return sent, tar # restituisce la lista delle frasi e la lista dei target separati relativi alle frasi


def column_from_dfO(csv_opinion):
    op=[] # lista vuota
    dfO = pd.read_csv(csv_opinion) # dataframe risultante dalla lettura del csv
    opinion = dfO['Opinion'].tolist() # estrapola la colonna delle parole di opinione
    new_opinion = ['NA' if x is np.nan else x for x in opinion] # rimpiazza i valori nan float con 'NA' stringa nella lista di parole di opinione
    for str in new_opinion: # new_opinion contiene una o più parole di opinione rilevate per ogni frase
        x = str.split() # in questo modo si suddividono le parole di opinione multiple per ogni frase
        # print(x)
        op.append(x) # in modo tale da inserirli nella lista tar come singoli
    return op # restituisce la lista delle parole di opinione separate relative alle frasi


# in input la lista delle parole di opinione estratte e i due lessici contenenti tutte le parole
# di opinione possibili e immaginabili
def polarity_lista(op, opinion_lexicon_positive, opinion_lexicon_negative):
    polarity = [] # lista vuota che conterrà le polarità
    for i in op: # per ogni lista di parola di opinione [bello, buono per frase1]
        pol = [] # lista vuota delle polarità
        for j in i: # # per ogni parola di opinione di una frase [j=bello prima iterata j=buono seconda iterata]
            with open(opinion_lexicon_positive) as f: # apertura file deelle parole di opinione positive
                with open(opinion_lexicon_negative) as f1: # apertura file deelle parole di opinione negative
                    if j in f.read():
                        pol.append('positive') # concatena la stringa 'positive' nella lista
                    elif j in f1.read():
                        pol.append('negative') # concatena la stringa 'negative' nella lista
                    else:
                        pol.append('NA') # concatena la stringa 'NA' nella lista se non trova polarità
        polarity.append(pol) # concatena le polarità trovate a una lista finale [bello+, buono+ per frase1]
    return polarity # restituisce la lista delle polarità


# ----------------metodi per la valutazione------------------------
# questo metodo riempie ogni elemento della lista con NA in base
# alla dimensione massima di target estratti per la frase massima
def process_lista_target(lista_target_estratti):
    n = len(max(lista_target_estratti, key=len)) # n conterrà la lunghezza massima delle stringhe target estratti per una frase in questo dataset n=7
    print(n)
    lista_target_estratti2 = [x + ['NA'] * (n - len(x)) for x in lista_target_estratti] # riempie la lista di 'NA' per itarget delle frasi che hanno meno di 7 target
    return n, lista_target_estratti2


# questo metodo riempie ogni elemento della lista con NA in base
# alla dimensione massima di target gold per la frase massima
def process_lista_target_gold(lista_target_gold, n): # prende in input n per inserire i NA in numero uguale alla lista_target_estratti
    # n1 = len(max(lista_target_gold, key=len)) # n1 conterrà la lunghezza massima delle stringhe target gold per una frase in questo dataset n1=6
    # n_tot=max(n,n1) # si dovrebbe fare così altrimenti se c'è una riga con più di 7 target si rischia di eliminare un target
    lista_target_gold2 = [x + ['NA1'] * (n - len(x)) for x in lista_target_gold] # riempie la lista di 'NA' per i target delle frasi che hanno meno di 7 target
    return lista_target_gold2


# questo metodo verifica il matching tra la lista dei target estratti con i 'NA'
# con la lista dei target gold con i 'NA1'
def lista_correct_target(lista_target_estratti_P, lista_target_gold_P):
    list_tmp = [] # lista vuota che conterrà gli elementi in comune
    # metodo zip combina la x=7-upla in pos 0 di lista_target_estratti_P con la y=7-upla in pos 0 di lista_target_gold_P
    for x, y in zip(lista_target_estratti_P, lista_target_gold_P):
        a = set(x).intersection(y) # a è l'insieme degli elementi in comune alle due 7-uple
        list_tmp.append(a) # aggiungo alla lista gli elementi in comune

    list_correct_target = []
    for item in list_tmp: # iterando sulla lista appena creata
        if item == set(): # se c'è un elemento vuoto (quindi con set())
            list_correct_target.append('no') # rimpiazzzalo con 'no'
        else:
            list_correct_target.append('si') # altrimenti inserisce 'si' per ogni parola rilevata (che sarebbe quella comune)
    # ciclo che conta quanti matching ha trovato in totale
    x = 0
    for i in list_correct_target:
        if i == 'si':
            x = x+1
    # restituisce la lista con si e no, il numero di si nella lista e la lunghezza della lista (ovvero numero di frasi)
    return list_correct_target, x, list_correct_target.__len__()


# ----------- i metodi seguenti effettuano le stesse operazioni dei metodi sopra descritti
# ma sfruttando la lista delle polarità estratte e a lista delle polarità gold -----------
def process_lista_polarity(lista_polarity_estratta):
    n = len(max(lista_polarity_estratta, key=len))
    # print(p)
    lista_polarity_estratta2 = [x + ['NA'] * (n - len(x)) for x in lista_polarity_estratta]
    return n, lista_polarity_estratta2


def process_lista_polarity_gold(lista_polarity_gold, n):
    lista_polarity_gold2 = [x + ['NA1'] * (n - len(x)) for x in lista_polarity_gold]
    return lista_polarity_gold2


def lista_corect_polarity(lista_polarity_estratta_P, lista_polarity_gold_P):
    list_tmp = []
    for x, y in zip(lista_polarity_estratta_P, lista_polarity_gold_P):
        a = set(x).intersection(y)
        list_tmp.append(a)
    # print(list)

    list_correct_polarity = []
    for item in list_tmp:
        if item == set():
            list_correct_polarity.append('no')
        else:
            list_correct_polarity.append('si')
    # print(list2.__len__())
    return list_correct_polarity
