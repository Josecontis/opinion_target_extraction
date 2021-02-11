import pandas as pd

from src import processing_data_to_target_polarity, evaluation, propagation, processing, processing_data
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

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
          "\n6) Process to add polarity to the targets and evaluate it"
          "\n7) Quit")

    choice = input("What would you like to do? Put your choice: ")

    if choice == "1":
        # creo il file del lessico di opinione
        processing_data.clean_sentiStrenght_txt(original_ss_file, processed_ss_file)
        processing_data.merge_txt(opinion_lexicon, processed_ss_file)

    elif choice == "2":
        # processing delle frasi del file csv in input
        processing_data.replace_symbols("../csv/target_annotation_dataset.csv", 'mydeveloper_comment')
        # processing dei target per le direzioni del file csv in input
        processing_data.replace_symbols("../processing_file_originale/Target_Annotation_Processed.csv", 'Target')

    elif choice == "3":
        # sentences contiene la lista di frasi e target_polarity la lista di target con polarità di ogni frase
        sentences, target_polarity = processing_data.csv_to_column_list(
            "../processing_file_originale/Target_Annotation_Processed.csv", 'mydeveloper_comment', 'myanger_direction')
        # algoritmo di doppia propagazione che prende in input la lista di frasi estratta dal csv e la libreria
        propagation.propagation(sentences, local_corenlp_path)

    elif choice == "4":
        processing_data.target_to_csv(target)
        processing_data.opinion_to_csv(opinion)

    elif choice == "5":
        # evaluation.tf_idf_extracted_words('../opinion.txt', 'TF-opinion-words')
        # evaluation.tf_idf_extracted_words('../target.txt', 'TF-targets')
        # evaluation.diff_files('../csv/Results/TF OW.txt', '../csv/Results/TF 2 OW.txt', '../csv/Results/Op_differences.txt')
        evaluation.diff_files('../csv/Results/TF target.txt', '../csv/Results/TF 2 target.txt', '../csv/Results/Tar_differences.txt')

    elif choice == "6":

        # a partire dal csv restituisce la lista delle frasi e la lista dei target estratti relativi alle frasi
        sentences, lista_target_gold, lista_target_estratti = processing.column_from_dfT(csv_target)
        print(lista_target_gold)
        print(lista_target_estratti)

        # INPUT: lista dei target estratti corretti e lista dei target gold corretti
        # OUTPUT: lista_target_correct è la lista di si e no, numero_corretti=48 è il numero
        # di target azzeccati, numero_totale=346 è il numero totale di frasi
        lista_target_correct, numero_corretti, numero_totale = processing.lista_correct_target(lista_target_estratti, lista_target_gold)
        print("n matched:", numero_corretti, "/", numero_totale)
        #valutazione target estratti
        # INPUT: numero_corretti=48 è il numero di target azzeccati, numero_totale=346 è il numero totale di frasi
        # OUTPUT: percentuale dei target estratti correttamente
        percentuale_corretti = evaluation.percentuale_targetEstratti_correct(numero_corretti, numero_totale)
        # percentuale di correttezza dell' estrazione dei target con 2 cifre decimali
        print('percentuale target corretti (accuracy): ', round(percentuale_corretti,2), '%')

        target_names = ['i', 'you', 'she', 'it', 'he']  # leave out '*'

        #print(classification_report(lista_target_gold, lista_target_estratti))

        #creazione del file .csv finale per visualizzare l'output
        df = pd.DataFrame()
        df['Sentence'] = sentences
        df['Target Estratti'] = lista_target_estratti
        df['Target Gold'] = lista_target_gold
        df['Correct Target'] = lista_target_correct


        df.to_csv('../csv/Final.csv', index=False)

    elif choice == "7":
        break

    a = input("\ndo you want to repeat the operations?  {y/n}  ")