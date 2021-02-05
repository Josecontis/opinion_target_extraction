import pandas as pd
import numpy as np
import re


# metodo per estrapolare le colonne da un file csv
def csv_to_column_list(file_csv, sentence_col, polarity_col):
    dfP = pd.read_csv(file_csv, encoding ='ISO-8859-1')  # lettura file csv delle polarità
    sentence = dfP[sentence_col].tolist()  # sentence contiene una lista di frasi estrapolate
    target_polarity = dfP[polarity_col].tolist()  # target_polarity contiene una lista di target con polarità estrapolate
    # per ogni elemento della lista di target con polarità vengono rimpiazzati i valori nan con 'NA1'
    new_target_polarity = ['NA1' if x is np.nan else x for x in target_polarity]
    return sentence, new_target_polarity  # restituisce la lista di frasi e la lista di target con polarità di ogni frase


# metodo per convertire txt to csv
def target_to_csv(targets_extracted):
    t = open(targets_extracted, 'r', encoding="utf8").readlines()  # apertura file in lettura
    list = [x.replace('\n', '').replace(',', '') for x in t]
    df = pd.read_csv('../processing_file_originale/Target_Annotation_Processed.csv')  # apre file Targ.csv in scrittura
    df['Targets'] = list
    df.to_csv('../csv/Targ.csv', index=False)


# metodo per convertire txt to csv
def opinion_to_csv(opinions_extracted):
    o = open(opinions_extracted, 'r', encoding="utf8").readlines()  # apertura file in lettura
    list = [x.replace('\n', '').replace(',', '') for x in o]
    df = pd.read_csv('../processing_file_originale/Target_Annotation_Processed.csv')  # apre file Targ.csv in scrittura
    df['Opinions'] = list
    df.to_csv('../csv/Opi.csv', index=False)


def replace_symbols(Original_file, col):
    # Read in the file
    file = pd.read_csv(Original_file, encoding="utf8")
    list_input = []
    list_output = []
    for x in file[col]:
        list_input.append(str(x))
    print(list_input)
    for phrase in list_input:
        m = re.findall(r'[@]\w+', phrase)  # trova i termini con il tag @
        for i in m:
            # sostituisco i termini con il tag @ con gli stessi ma con il primo carattere maiuscolo
            phrase = phrase.replace(i, i.title())

        # sostituisco le short words
        phrase = re.sub(r"won't", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)

        phrase = re.sub(r"\'re ", " are ", phrase)
        phrase = re.sub(r"\'s ", " is ", phrase)
        phrase = re.sub(r"\'d ", " would ", phrase)
        phrase = re.sub(r"\'ll ", " will ", phrase)
        phrase = re.sub(r"\'ve ", " have ", phrase)
        phrase = re.sub(r"\'m ", " am ", phrase)


        #print(filedata[col])
        # rimozione dei caratteri inutili in filedata
        phrase = phrase.replace('%', '')
        phrase = phrase.replace(';', '')
        phrase = phrase.replace('*', '')
        phrase = phrase.replace('@', '')
        phrase = phrase.replace('\\', '')
        phrase = phrase.replace('#', '')
        phrase = phrase.replace('$', '')
        phrase = phrase.replace('^', '.')
        phrase = phrase.replace('"', '')
        phrase = phrase.replace('~', '')
        phrase = phrase.replace('--', '')
        phrase = phrase.replace('>>>', '')
        phrase = phrase.replace('///', '')
        phrase = phrase.replace('<=', '')
        # rimozione di parentesi {} che non hanno una chiusura o apertura
        phrase = phrase.replace('{ ', '')
        phrase = phrase.replace(' }', '')
        if col=='mydeveloper_comment':
            phrase = phrase.replace('(', '')
            phrase = phrase.replace(')', '')
        phrase = phrase.replace(':', '')
        # rimozione carattere di punto elenco ma non di mezzi termini (che non hanno gli spazi)
        phrase = phrase.replace('- ', '')

        phrase = re.sub(r"<[^>]*>", "", phrase)  # rimuove XML tags
        phrase = re.sub(r"{[^}]*}", "", phrase)  # rimuove codici tra parentesi {}
        phrase = re.sub(r"[\[].*?[\]]", "", phrase)  # rimuove nomi e operazioni tra parentesi []
        phrase = re.sub(r"http\S+", "", phrase)  # rimuove codici URL
        phrase = re.sub(r"https\S+", "", phrase)  # rimuove codici URL

        phrase = phrase.replace('>', '')
        phrase = phrase.replace('}', '')
        phrase = phrase.replace('//', ' ')
        phrase = phrase.replace(',', ' ')

        phrase = re.sub(r"n't ", " not ", phrase)  # rimuove codici URL

        # rimozione spazi vuoti lasciati
        phrase = phrase.replace('    ', ' ')
        phrase = phrase.replace('   ', ' ')
        phrase = phrase.replace('  ', ' ')

        list_output.append(phrase)

    file[col] = list_output
    file.to_csv('../processing_file_originale/Target_Annotation_Processed.csv', index=False)

# metodo per unire il contenuto di due documenti di testo
def merge_txt(neg_file, pos_file):

    # creo la lista dei file da esaminare
    filenames = [neg_file, pos_file]

    # apro il file di output in scrittura
    with open('../opinion-lexicon-English/Opinion-lexicon.txt', 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                # leggo il contenuto del primo file di input e lo scrivo nel file di output
                outfile.write(infile.read())

'''
# ------ non utilizzato nel main -----
def rimozione_titoli_t(file_originale_caratteri_rimpiazzati):
    # rimuove le righe dal file che rappresenano i titoli denominati con [t]
    file1 = open(file_originale_caratteri_rimpiazzati) # apre file da modificare
    file2 = open('../processing_file_originale/Nikon coolpix 4300.Copia2.txt', 'w') # crea nuovo file per l'output

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
    sentence, target_polarity = csv_to_column_list(file_csv) # estrapola colonna frasi e target con le polarità
    with open(file, 'w') as f: # con il file .txt aperto in scrittura
        for item in sentence: # itera sulle frasi
            f.write("%s\n" % item) # scrive nel file .txt la frase


# ------ non utilizzato nel main -----
def process_file(file_originale_processato):
    with open(file_originale_processato) as f:
        with open(file_prova, 'w') as f1:
            for line in f:
                f1.write(re.sub(r'([]])([a-z])', r'\1 \2', line))


file_Originale = '../processing_file_originale/Nikon coolpix 4300.txt'
file_originale_caratteri_rimpiazzati = '../processing_file_originale/Nikon coolpix 4300-Copia.txt'
file_originale_processato = '../processing_file_originale/Nikon coolpix 4300.Copia2.txt'
file_originale_processato_csv = '../csv/Gold.csv'
input = '../input.txt'
file_prova = '../processing_file_originale/Nikon coolpix 4300.Copia2 - Copia.txt'

'''

#rimozione_titoli_t(file_originale_caratteri_rimpiazzati)
#process_file(file_originale_processato)
#trasforma_in_csv(file_prova)
#scrivere_sentence_file(input, file_originale_processato_csv)

