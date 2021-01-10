from src import rule
import nltk
from nltk.tokenize import sent_tokenize

# nel caso di un testo, viene suddiviso lo stesso in una lista di frasi
'''
def sentence_tokenize(input):
    nltk.download('punkt')
    text = open("../input.txt").read()
    sentences = sent_tokenize(text)
    return sentences
'''

def propagation(sentences, local_corenlp_path): # questo metodo prende in input la lista di frasi e la libreria

    #sentences = sentence_tokenize(input)

    for input in sentences: # per ogni singola frase nella lista di frasi

        target = open('../target.txt', 'a') # apre il file dei target inizialmente vuoto in append
        opinion = open('../opinion.txt', 'a') # apre il file delle parole di opinione inizialmente vuoto in append

        target.write('\n') # ritorno a capo per l'append di nuove frasi
        target.write(input +'#') # inserimento di # dopo la frase
        opinion.write('\n') # ritorno a capo per l'append di nuove frasi
        opinion.write(input + '#') # inserimento di # dopo la frase

        print("REGOLA 1")
        print('\n')
        targ = rule.R1(local_corenlp_path, input) # estrapolazione del target tramite la regola R1, passando
                                                    # al metodo la libreria e la frase da esaminare
        for element in targ:    # targ è la lista di tutti i target estratti dalla singola frase (ovvero input)
            target.write(' ')   # scrive uno spazio nel file dopo #
            target.write(element)  # scrive nel file i target trovati
            target.write(' ')  # scrive uno spazio nel file dopo il target per separlo con un altro alla prossima iterata

        target = '../lessico_target_opinion/Lessico-Target.txt' # la variabile viene aggiornata con il file dei target singoli estratti prima
        print("REGOLA 2")
        print('\n')
        opin = rule.R2(local_corenlp_path, input, target)# estrapolazione della parola di opinione tramite la regola R2, passando
                                                    # al metodo la libreria e la frase da esaminare, e il file dei target singoli estratti prima
        for element in opin: # opin è la lista di tutte le parola di opinione estratte dalla singola frase (ovvero input)
            opinion.write(' ') # scrive uno spazio nel file dopo #
            opinion.write(element) # scrive nel file la parola di opinione trovate
            opinion.write(' ') # scrive uno spazio nel file dopo la parola di opinione per separlo con un altra alla prossima iterata

        target = open('../target.txt', 'a') # apre il file dei target ora non vuoto in append
        targe = '../lessico_target_opinion/Lessico-Target.txt' # la variabile targe è il file dei target singoli estratti prima
        print("REGOLA 3")
        print('\n')
        targ = rule.R3(local_corenlp_path, input, targe)# estrapolazione del target tramite la regola R3, passando
                                                    # al metodo la libreria, la frase da esaminare e il file dei target singoli estratti prima
        for element in targ:
            target.write(' ') # scrive uno spazio nel file dopo #
            target.write(element) # scrive nel file i target trovati
            target.write(' ') # scrive uno spazio nel file dopo il target per separlo con un altro alla prossima iterata

        opinion = open('../opinion.txt', 'a') # apre il file delle parole di opinione ora non vuoto in append
        opin = '../lessico_target_opinion/Lessico-Opinion.txt'# la variabile opin è il file delle parole di opinione singole estratti prima
        print("REGOLA 4")
        print('\n')
        op = rule.R4(local_corenlp_path, input, opin) # estrapolazione della parola di opinione tramite la regola R4, passando
                                                    # al metodo la libreria, la frase da esaminare e il file dei target singoli estratti prima
        for element in op:
            opinion.write(' ') # scrive uno spazio nel file dopo #
            opinion.write(element) # scrive nel file la parola di opinione trovate
            opinion.write(' ') # scrive uno spazio nel file dopo la parola di opinione per separlo con un altra alla prossima iterata

        target.close() # chiusura del file dei target estratti
        opinion.close() # chiusura del file delle parole di opinione estratte