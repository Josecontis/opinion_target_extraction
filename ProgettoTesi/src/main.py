import pandas as pd

from src import processing_data_to_target_polarity, evaluation, propagation, processing, processing_data
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report, accuracy_score

# espande il display di output per visualizzare più righe e colonne
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 2000)

local_corenlp_path = '../stanford-corenlp-4.2.0'
csv = '../processing_fileOriginale/GOLD_723_processed.csv'
target = '../target.txt'
opinion = '../opinion.txt'
lexicon_positive = '../opinion-lexicon-English/positive-words.txt'
lexicon_negative = '../opinion-lexicon-English/negative-words.txt'
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
          "\n6) Process to add polarity to the targets and evaluate it"
          "\n7) Quit")

    choice = input("What would you like to do? Put your choice: ")

    if choice == "1":
        # creo il file del lessico di opinione
        processing_data.merge_txt(lexicon_positive, lexicon_negative)

    elif choice == "2":
        # processing del file csv in input
        processing_data.replace_symbols("../csv/target_annotation_dataset.csv")

    elif choice == "3":
        # sentences contiene la lista di frasi e target_polarity la lista di target con polarità di ogni frase
        sentences, target_polarity = processing_data.csv_to_column_list("../processing_fileOriginale/Target_Annotation_Processed.csv", 'mydeveloper_comment', 'myanger_direction')
        # algoritmo di doppia propagazione che prende in input la lista di frasi estratta dal csv e la libreria
        propagation.propagation(sentences, local_corenlp_path)

    elif choice == "4":
        processing_data.target_to_csv(target)
        processing_data.opinion_to_csv(opinion)

    elif choice == "5":
        # evaluation.tf_idf_extracted_words('../opinion.txt', 'TF-opinion-words')
        # evaluation.tf_idf_extracted_words('../target.txt', 'TF-targets')
        evaluation.diff_files('../csv/Results/TF OW.txt', '../csv/Results/TF 2 OW.txt', '../csv/Results/Op_differences.txt')
        evaluation.diff_files('../csv/Results/TF target.txt', '../csv/Results/TF 2 target.txt', '../csv/Results/Tar_differences.txt')

    elif choice == "6":
        # a partire dal csv restituisce la lista delle parole di opinione separate relative alle frasi
        lista_opinion_estratti = processing.column_from_dfO(csv_opinion)
        # a partire dalla lista di parole di opinione estratte e i due lessici contenenti tutte le parole
        # di opinione possibili e immaginabili si estrae una lista di polarità delle parole di opinione
        lista_polarity_estratta = processing.polarity_lista(lista_opinion_estratti, lexicon_positive, lexicon_negative)

        # INPUT: la lista dei target con le polarità unite ed estratte dal csv gold
        # OUTPUT: la lista dei target con le polarità separate
        list_target_polarity = processing_data_to_target_polarity.process_list_target_polarity(target_polarity)

        # INPUT: la lista dei target con le polarità separate
        # OUTPUT: solo la lista dei target di tutte le frasi
        lista_target_gold = processing_data_to_target_polarity.listaTarget_from_listaTargetPolarity(list_target_polarity)

        # INPUT: la lista dei target con le polarità separate
        # OUTPUT: solo la lista delle polarità di tutte le frasi
        lista_polarity_gold = processing_data_to_target_polarity.listaPolarity_from_listaTargetPolarity(list_target_polarity)

        # INPUT: la lista dei target con SOLO le polarità [es. (+3),(-2)...]
        # OUTPUT: la lista delle polarità stringhe di tutte le frasi [es. (positive),(negative)...]
        lista_polarity_gold_mod = processing_data_to_target_polarity.process_list_polarity_gold(lista_polarity_gold)

        # a partire dal csv restituisce la lista delle frasi e la lista dei target estratti relativi alle frasi
        sentence, lista_target_estratti = processing.column_from_dfT(csv_target)

        # ----------rende le due liste con dimensioni uguali per la
        # valutazione tramite intersezione degli elementi comuni------------

        # INPUT: lista dei target estratti
        # OUTPUT: la lista dei target corretti di dimensione agggiungendo 'NA', ed n è
        # la lunghezza massima delle stringhe target estratti per una frase
        n, lista_target_estratti_P = processing.process_lista_target(lista_target_estratti)

        # INPUT: lista dei target gold e n la dimensione per correggere la lista dei target gold con i 'NA1'
        # OUTPUT: la lista dei target gold corretti di dimensione agggiungendo 'NA1'
        lista_target_gold_P = processing.process_lista_target_gold(lista_target_gold, n)

        # INPUT: lista dei target estratti corretti e lista dei target gold corretti
        # OUTPUT: lista_target_correct è la lista di si e no, numero_corretti=48 è il numero
        # di target azzeccati, numero_totale=346 è il numero totale di frasi
        lista_target_correct, numero_corretti, numero_totale = processing.lista_correct_target(lista_target_estratti_P, lista_target_gold_P)

        # stessa cosa precedente ma per la lista delle polarità estratte con la lista delle polarità gold
        n, lista_polarity_estratta_P = processing.process_lista_polarity(lista_polarity_estratta)
        lista_polarity_gold_P = processing.process_lista_target_gold(lista_polarity_gold_mod, n)
        lista_polarity_correct = processing.lista_corect_polarity(lista_polarity_estratta_P, lista_polarity_gold_P)

        #valutazione target estratti
        # INPUT: numero_corretti=48 è il numero di target azzeccati, numero_totale=346 è il numero totale di frasi
        # OUTPUT: percentuale dei target estratti correttamente
        percentuale_corretti = evaluation.percentuale_targetEstratti_correct(numero_corretti, numero_totale)
        # percentuale di correttezza dell' estrazione dei target con 2 cifre decimali
        print('percentuale target corretti: ', round(percentuale_corretti,2), '%')

        #valutazione polarità estratte
        # metodo che crea dei vettori binari che rappresentano la presenza(1) o assenza(0)
        # di ogni classe per ogni frase (dove le classi sono NA,positive e negative)
        mlb = MultiLabelBinarizer()
        lista_polarity_gold_mod_tr = mlb.fit_transform(lista_polarity_gold_mod)
        lista_polarity_estratta_tr = mlb.fit_transform(lista_polarity_estratta)
        classes = list(mlb.classes_) # classes contiene i possibili valori

        #metodo che stampa i valori delle metriche:
        #               precision    recall  f1-score   support
        #     NA            n           n       n         n
        #     positive      n           n       n         n
        #     negative      n           n       n         n
        print(classification_report(lista_polarity_gold_mod_tr,lista_polarity_estratta_tr, target_names=classes))

        # stampa l'accuratezza arrotondata a 2 cifre decimali del matching tra polarità estratte e polarità gold
        print('accuracy:', round(accuracy_score(lista_polarity_gold_mod_tr, lista_polarity_estratta_tr),2))

        # visualizzazione della matrice di confusione
        evaluation.confusionMatrix(lista_polarity_gold_mod_tr.argmax(axis=1), lista_polarity_estratta_tr.argmax(axis=1), classes, name='Confusion Matrix')

        #creazione del file .csv finale per visualizzare l'output
        df = pd.DataFrame()
        df['Sentence'] = sentences
        df['Target Estratti'] = lista_target_estratti
        df['Target Gold'] = lista_target_gold
        df['Correct Target'] = lista_target_correct
        df['Opinion Estratti'] = lista_opinion_estratti
        df['Polarity Estratta'] = lista_polarity_estratta
        df['Polarity Gold'] = lista_polarity_gold_mod
        df['Correct Polarity'] = lista_polarity_correct

        df.to_csv('../csv/Final.csv')

    elif choice == "7":
        break

    a = input("\ndo you want to repeat the operations?  {y/n}  ")