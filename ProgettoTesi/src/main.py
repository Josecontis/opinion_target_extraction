import pandas as pd
from src import evaluation, propagation, processing, processing_data


# espande il display di output per visualizzare più righe e colonne
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 2000)

local_corenlp_path = '../stanford-corenlp-4.2.0'
csv = '../processing_file_originale/GOLD_723_processed.csv'
target = '../target.txt'
opinion = '../opinion.txt'
original_ss_file = '../opinion-lexicon-English/EmotionLookupTable.txt'
processed_ss_file = '../opinion-lexicon-English/EmotionLookupTableProcessed.txt'
opinion_lexicon = '../opinion-lexicon-English/Opinion-lexicon.txt'
csv_target = '../csv/Targ.csv'
csv_opinion = '../csv/Opi.csv'

a = 'y'
while a == 'y':

    print("\nPossible choices:")
    print("1) create opinion lexicon"
          "\n2) data processing and sentence capture"
          "\n3) Double propagation to extract targets and opinion words"
          "\n4) Setting results of extraction into two csv files"
          "\n5) evaluate extraction process"
          "\n6) Process to evaluate target extraction process"
          "\n7) Quit")

    choice = input("What would you like to do? Put your choice: ")

    if choice == "1":
        # creo il file del lessico di opinione
        processing_data.clean_sentiStrenght_txt(original_ss_file, processed_ss_file)
        processing_data.append_txt(opinion_lexicon, processed_ss_file)

    elif choice == "2":
        # processing delle frasi del file csv in input
        processing_data.replace_symbols("../csv/target_annotation_dataset.csv", 'mydeveloper_comment')
        # processing dei target per le direzioni del file csv in input
        processing_data.replace_symbols("../processing_file_originale/Target_Annotation_Processed.csv", 'Target')

    elif choice == "3":
        # sentences contiene la lista di frasi prese dal csv
        sentences = processing_data.csv_to_column_list("../processing_file_originale/Target_Annotation_Processed.csv", 'mydeveloper_comment')
        # algoritmo di doppia propagazione che prende in input la lista di frasi estratta dal csv e la
        # libreria ed estrae target e parole di opinione
        propagation.propagation(sentences, local_corenlp_path)

    elif choice == "4":
        # unisce i due file txt poichè come colonna gold di target si hanno sia nomi che pronomi...
        processing_data.merge_txt('../target.txt', '../Target_nouns.txt')
        # crea un nuovo csv per inserire i target estratti sia come nomi che pronomi...
        processing_data.target_to_csv('../res.txt')
        # crea un nuovo csv per inserire le parole di opinione estratte
        processing_data.opinion_to_csv(opinion)

    elif choice == "5":
        # metodo di valutazione basato sulle frequenze delle parole di opinione estratte
        # evaluation.tf_idf_extracted_words('../opinion.txt', 'TF-opinion-words')
        # metodo di valutazione basato sulle frequenze dei target estratti
        # evaluation.tf_idf_extracted_words('../target.txt', 'TF-targets')
        # metodo di valutazone delle differenze in base alle frequenze su 2 analisi diverse scritte su file sia pr parole di opinione che per target
        evaluation.diff_files('../csv/Results/TF OW.txt', '../csv/Results/TF 2 OW.txt', '../csv/Results/Op_differences.txt')
        evaluation.diff_files('../csv/Results/TF target.txt', '../csv/Results/TF 2 target.txt', '../csv/Results/Tar_differences.txt')

    elif choice == "6":

        # a partire dal csv restituisce la lista delle frasi, la lista dei target gold e la lista dei target estratti
        sentences, lista_target_gold, lista_target_extracted = processing.column_from_dfT(csv_target)
        lista_opinion_extracted = processing.column_from_dfO(csv_opinion)


        # INPUT: lista dei target estratti e lista dei target gold
        # OUTPUT: lista_target_correct è la lista di si e no, numero_corretti = è il numero
        # di target azzeccati, numero_totale = è il numero totale di frasi
        lista_target_correct, numero_corretti, numero_totale = processing.lista_correct_target(lista_target_extracted, lista_target_gold)
        print("n matched:", numero_corretti, "/", numero_totale)
        #valutazione target estratti
        # INPUT: numero_corretti è il numero di target azzeccati, numero_totale è il numero totale di frasi
        # OUTPUT: percentuale dei target estratti correttamente
        percentuale_corretti = evaluation.percenage_correct_target_extracted(numero_corretti, numero_totale)
        # percentuale di correttezza dell' estrazione dei target con 2 cifre decimali
        print('percentuale target corretti: ', round(percentuale_corretti, 2), '%')

        #creazione del file .csv finale per visualizzare l'output
        df = pd.DataFrame()
        df['Sentence'] = sentences
        df['Target Gold'] = lista_target_gold
        df['Extracted Target'] = lista_target_extracted
        df['Correct Target'] = lista_target_correct
        df['Extracted Opinion'] = lista_opinion_extracted
        df['Note'] = ""
        df['Problem Cat.'] = ""
        df['POS'] = ""
        df['DEP'] = ""

        df.to_csv('../csv/Final.csv', index=False)

    elif choice == "7":
        break

    a = input("\ndo you want to repeat the operations?  {y/n}  ")