import pandas as pd
import re


# metodo per estrapolare le colonne da un file csv
def csv_to_column_list(file_csv, sentence_col):
    dfP = pd.read_csv(file_csv, encoding ='ISO-8859-1')  # lettura file csv delle polarità
    sentence = dfP[sentence_col].tolist()  # sentence contiene una lista di frasi estrapolate
    return sentence  # restituisce la lista di frasi e la lista di target con polarità di ogni frase


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
def append_txt(neg_file, pos_file):

    # creo la lista dei file da esaminare
    filenames = [neg_file, pos_file]

    # apro il file di output in scrittura
    with open('../opinion-lexicon-English/Opinion-lexicon-with-ss.txt', 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                # leggo il contenuto del primo file di input e lo scrivo nel file di output
                outfile.write(infile.read())

# metodo per unire il contenuto di due documenti di testo
def merge_txt(file1, file2):
    combine = []

    with open(file1) as xh:
        with open(file2) as yh:
            with open("../res.txt", "w") as zh:
                # Read first file
                xlines = xh.readlines()
                # Read second file
                ylines = yh.readlines()
                # Combine content of both lists
                # combine = list(zip(ylines,xlines))
                # Write to third file

                for i in range(len(xlines)):
                    if ylines[i] == "\n":
                        line = ylines[i].strip() + '' + xlines[i]
                        zh.write(line)
                    else:
                        line = ylines[i].strip() + ' ' + xlines[i]
                        zh.write(line)

def clean_sentiStrenght_txt(o_file, p_file):

    # apro il file di output in scrittura
    words=[]
    with open(o_file, 'r') as op_file:
        for line in op_file:
            sep = '\t'
            stripped = line.split(sep, 1)[0]
            words.append(stripped)
    with open(p_file, "w") as file:
        for e in words:
          file.write(str(e) + '\n')

