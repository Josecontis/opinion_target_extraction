import difflib

def tf_idf_extracted_words(file, title):
    t = open(file, 'r').readlines()  # apertura file in lettura
    list = [x.replace('\n', '').replace(',', '') for x in t]
    l = [words for segments in list for words in segments.split()]

    # Creating an empty dictionary
    freq = {}
    for item in l:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    print(title)
    for key, value in freq.items():
        print("% s : % d" % (key, value))


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

