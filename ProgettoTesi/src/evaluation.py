from sklearn import metrics
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


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


    # in input numero dei target estratti corretti e il numero dei target estratti totali
def percentuale_targetEstratti_correct(n_correct, n_total):
    percent = ((n_correct/n_total)*100) # calcolo della percentuale per indicare i target azzeccati
    return percent


# classes name: positive negative NA, name: 'confusion matrix', gold: lista delle polarità gold, prediction: lista
# delle polarità estratte
def confusionMatrix(gold, prediction, classes_name, name):
    # Plot non-normalized confusion matrix
    matrix = metrics.confusion_matrix(gold, prediction)
    plt.figure(figsize=(6, 4))
    sns.heatmap(matrix,
                cmap='coolwarm',
                linecolor='white',
                linewidths=1,
                xticklabels=classes_name,
                yticklabels=classes_name,
                annot=True,
                fmt='d')
    plt.title(name)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
