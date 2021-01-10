from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt


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
