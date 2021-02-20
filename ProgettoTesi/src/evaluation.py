import difflib


# questo metodo di valutazione è legato alle frequenze ovvero conta quanti termini sono stati estratti
def tf_idf_extracted_words(file, title):
    t = open(file, 'r').readlines()  # apertura file in lettura
    list = [x.replace('\n', '').replace(',', '') for x in t]  # rimpiazza caratteri inutili dal file e inserisce il contenuto in una lista
    l = [words for segments in list for words in segments.split()]

    # crea un dizionario dove va ad inserire termine come chiave e frequenza come valore
    freq = {}
    for item in l:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    print(title)
    for key, value in freq.items():
        print("% s : % d" % (key, value))


# questo metodo di valutazione confronta due file di frequenze di termini e restituisce i risultati in un nuovo file
def diff_files(files1, files2, output):

    text1 = open(files1).readlines()
    text2 = open(files2).readlines()

    with open(output, 'w') as file_out:
        for line in difflib.unified_diff(text1, text2):
            file_out.write(line)


    # in input numero dei target estratti corretti e il numero dei target estratti totali
def percenage_correct_target_extracted(n_correct, n_total):
    percent = ((n_correct/n_total)*100) # calcolo della percentuale per indicare i target azzeccati
    return percent

