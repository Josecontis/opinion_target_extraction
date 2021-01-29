from src import rule


def search_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as file_op:
        # For each line, check if line contains the string
        for line in file_op:
            if string_to_search+"\n" == line:
                return True
    return False


def propagation(sentences, local_corenlp_path):  # questo metodo prende in input la lista di frasi e la libreria

    for phrase in sentences:  # per ogni singola frase nella lista di frasi

        with open('../target.txt', 'a') as file_tar_r1:  # apre il file dei target inizialmente vuoto in append
            opinion = '../opinion-lexicon-English/Opinion-lexicon.txt'  # lessico di opinione delle parole positive
            print("REGOLA 1")
            print('\n')
            tar_r1 = rule.R1(local_corenlp_path, phrase, opinion)  # estrapolazione del target tramite la regola R1, passando
                                                          # al metodo la libreria e la frase da esaminare

            file_tar_r1.write('\n')  # ritorna a capo per scrivere nuovi target
            for word_r1 in tar_r1:  # targ è la lista di tutti i target estratti dalla singola frase (ovvero input)
                file_tar_r1.write(word_r1)  # scrive nel file i target trovati
                file_tar_r1.write(', ')  # scrive uno spazio nel file dopo il target per separlo con un altro alla prossima iterata

        with open('../opinion.txt', 'a') as file_opi_r2:
            with open('../opinion-lexicon-English/Opinion-lexicon.txt', 'a+') as lex_opi_r2:
                target = '../target.txt'  # la variabile viene aggiornata con il file dei target singoli estratti prima
                print("REGOLA 2")
                print('\n')
                opi_r2 = rule.R2(local_corenlp_path, phrase, target)  # estrapolazione della parola di opinione tramite la regola R2, passando
                                                        # al metodo la libreria e la frase da esaminare, e il file dei target singoli estratti prima

                file_opi_r2.write('\n')  # ritorna a capo per scrivere nuove parole di opinione
                for word_r2 in opi_r2:  # opin è la lista di tutte le parola di opinione estratte dalla singola frase (ovvero input)
                    file_opi_r2.write(word_r2)  # scrive nel file la parola di opinione trovate
                    file_opi_r2.write(', ')  # scrive uno spazio nel file dopo la parola di opinione per separlo con un altra alla prossima iterata

                for word_r2 in opi_r2:  # opin è la lista di tutte le parola di opinione estratte dalla singola frase (ovvero input)
                    if not search_string_in_file('../opinion-lexicon-English/Opinion-lexicon.txt', word_r2):
                        lex_opi_r2.write(word_r2)  # scrive nel file la parola di opinione trovate
                        lex_opi_r2.write('\n')  # ritorna a capo per scrivere nuove parole di opinione

        with open('../target.txt', 'a') as file_tar_r3:  # apre il file dei target inizialmente vuoto in append
            targe = '../target.txt'
            print("REGOLA 3")
            print('\n')
            tar_r3 = rule.R3(local_corenlp_path, phrase, targe)  # estrapolazione del target tramite la regola R3, passando
                                                        # al metodo la libreria, la frase da esaminare e il file dei target singoli estratti prima

            for word_r3 in tar_r3:
                file_tar_r3.write(word_r3)  # scrive nel file i target trovati
                file_tar_r3.write(', ')  # scrive uno spazio nel file dopo il target per separlo con un altro alla prossima iterata

        with open('../opinion.txt', 'a') as file_opi_r4:
            with open('../opinion-lexicon-English/Opinion-lexicon.txt', 'a+') as lex_opi_r4:
                opin = '../opinion-lexicon-English/Opinion-lexicon.txt' # la variabile opin è il file delle parole di opinione singole estratti prima
                print("REGOLA 4")
                print('\n')
                opi_r4 = rule.R4(local_corenlp_path, phrase, opin)  # estrapolazione della parola di opinione tramite la regola R4, passando
                                                                    # al metodo la libreria, la frase da esaminare e il file dei target singoli estratti prima

                for word_r4 in opi_r4:
                    file_opi_r4.write(word_r4)  # scrive nel file la parola di opinione trovate
                    file_opi_r4.write(', ')  # scrive uno spazio nel file dopo la parola di opinione per separlo con un altra alla prossima iterata

                for word_r4 in opi_r4:  # opin è la lista di tutte le parola di opinione estratte dalla singola frase (ovvero input)
                    if not search_string_in_file('../opinion-lexicon-English/Opinion-lexicon.txt', word_r4):
                        lex_opi_r4.write(word_r4)  # scrive nel file la parola di opinione trovate
                        lex_opi_r4.write('\n')  # ritorna a capo per scrivere nuove parole di opinione

    file_tar_r1.close()  # chiusura del file dei target estratti
    file_tar_r3.close()  # chiusura del file dei target estratti
    file_opi_r2.close()  # chiusura del file delle parole di opinione estratte
    file_opi_r4.close()  # chiusura del file delle parole di opinione estratte
    lex_opi_r2.close()  # chiusura del lessico delle parole di opinione esteso
    lex_opi_r4.close()  # chiusura del lessico delle parole di opinione esteso
