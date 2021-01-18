import pandas as pd
import numpy as np
import csv

# ------------------- OPERAZIONI PER CREARE GOLD.CSV A PARTIRE DEL DATASET NIKON COOLPIX 4300 --------------------

# metodo per estrapolare le colonne da un file csv
def csv_to_column_list(file_csv, sentence_col, polarity_col):
    dfP = pd.read_csv(file_csv, encoding = "ISO-8859-1") # lettura file csv delle polarità
    sentence = dfP[sentence_col].tolist() # sentence contiene una lista di frasi estrapolate
    target_polarity = dfP[polarity_col].tolist() # target_polarity contiene una lista di target con polarità estrapolate
    # per ogni elemento della lista di target con polarità vengono rimpiazzati i valori nan con 'NA1'
    new_target_polarity = ['NA1' if x is np.nan else x for x in target_polarity]
    return sentence, new_target_polarity # restituisce la lista di frasi e la lista di target con polarità di ogni frase

# metodo per convertire txt to csv
def target_to_csv(words_extracted, sentences):
    with open(words_extracted, 'r') as in_file: # apertura file in lettura
        lines = (line.split("\n") for line in in_file) # lines è un vettore con es. (frase, target)...
        print(lines)
        with open('../csv/Targ.csv', 'w', newline='') as out_file: # apre file Targ.csv in scrittura
            writer = csv.writer(out_file) # copia il contenuto in writer
            writer.writerow(('Sentences', 'Targets')) # scrive la prima riga per indicare le colonne
            row = zip(sentences, lines)
            writer.writerows(row) # scrive le linee restanti


def replace_symbols(file_Originale):
    # Read in the file
    with open(file_Originale, 'r') as file: # apre il file originale in lettura
        filedata = file.read() # salva il contenuto in filedata

    # rimpiazza i diversi caratteri, non utili in fileadta
    filedata = filedata.replace('?', '.')
    filedata = filedata.replace('!', '.')
    filedata = filedata.replace('%', '')
    filedata = filedata.replace(';', '')
    filedata = filedata.replace('*', '')
    filedata = filedata.replace('/', '')
    filedata = filedata.replace('(', '')
    filedata = filedata.replace(')', '')
    filedata = filedata.replace('-', '')
    filedata = filedata.replace('@', '')
    filedata = filedata.replace('\\', '')
    filedata = filedata.replace(':', '.')
    filedata = filedata.replace('#', '')
    filedata = filedata.replace('$', '')
    filedata = filedata.replace('^', '.')
    filedata = filedata.replace('"', '')
    filedata = filedata.replace('~', '')
    filedata = filedata.replace('>>>', '')
    filedata = filedata.replace('  ', ' ')
    filedata = filedata.replace('   ', ' ')
    filedata = filedata.replace('    ', ' ')

    # scrive il file precedente in un altro privato dei caratteri rimpiazzati
    with open('../processing_fileOriginale/GOLD_723_processed.csv', 'w') as file:
        file.write(filedata)

'''
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


file_Originale = '../processing_fileOriginale/Nikon coolpix 4300.txt'
file_originale_caratteri_rimpiazzati = '../processing_fileOriginale/Nikon coolpix 4300-Copia.txt'
file_originale_processato = '../processing_fileOriginale/Nikon coolpix 4300.Copia2.txt'
file_originale_processato_csv = '../csv/Gold.csv'
input = '../input.txt'
file_prova = '../processing_fileOriginale/Nikon coolpix 4300.Copia2 - Copia.txt'

'''

#rimozione_titoli_t(file_originale_caratteri_rimpiazzati)
#process_file(file_originale_processato)
#trasforma_in_csv(file_prova)
#scrivere_sentence_file(input, file_originale_processato_csv)

