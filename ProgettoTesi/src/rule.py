from stanfordcorenlp import StanfordCoreNLP
import logging
import numpy as np


def SC(local_corenlp_path, input):  # in input la libreria e la frase da esaminare
  # in input la libreria, quiet se falso fa visualizzare i messaggi di info del server durante l'esecuzione
  # logging_level indica il modo per ottenere i log dalle funzioni remote
  nlp = StanfordCoreNLP(local_corenlp_path, quiet=True, logging_level=logging.DEBUG) # nlp è il "processo" server

  Tokenize = nlp.word_tokenize(input)  # tokenizer per suddividere le singole parole della frase input
  POS = nlp.pos_tag(input)  # assegno i tag pos(jj aggettivo, NN nome ecc..) alle singole parole della frase input
  Dependency = nlp.dependency_parse(input)  # costruisce l'albero delle dipendenze sulle singole parole della frase input
  nlp.close()  # termina processo server
  return Tokenize, POS, Dependency  # 3 liste, esempi:
  # Tokenize ['il', 'pc', 'è', 'performante']
  # POS [('il', 'DT'), ('pc', 'NN'), ('è', 'VRB'), ('performante', 'JJ')]
  # Dependency [('il', 'DT'), ('pc', 'NN'), ('è', 'VRB'), ('performante', 'JJ')]



def R1(local_corenlp_path, input):  # in input la libreria e la frase da esaminare

  toke, pos, depe = SC(local_corenlp_path, input)  # richiamo metodo per tokenizer tag pos e albero delle dipendenze
  # esempio di frase: iPod is the best mp3 player.
  # Tokeninze:  ['iPod', 'is', 'the', 'best', 'mp3', 'player', '.']
  # Part Of Speech:  [('iPod', 'NN'), ('is', 'VBZ'), ('the', 'DT'), ('best', 'JJS'), ('mp3', 'NN'), ('player', 'NN'), ('.', '.')]
  # Dependency Parse:  [('ROOT', 0, 6), ('nsubj', 6, 1), ('cop', 6, 2), ('det', 6, 3), ('amod', 6, 4), ('compound', 6, 5), ('punct', 6, 7)]Tokeninze:  ['this', 'camera', 'is', 'perfect', 'for', 'an', 'enthusiastic', 'amateur', 'photographer', '.']

  # stampa operazioni fatte
  print("Tokeninze: ", toke)
  print('\n')
  print("Part Of Speech: ", pos)
  print('\n')
  print("Dependency Parse: ", depe)
  print('\n')

  tok = np.array(toke)  # tok è l'array di singole parole in una frase
  list_target = []  # lista vuota che conterrà i target

  Op = '../opinion-lexicon-English/positive-words.txt'  # lessico di opinione delle parole positive
  On = '../opinion-lexicon-English/negative-words.txt'  # lessico di opinione delle parole negative
  val = ['JJ', 'JJS', 'JJR'] # array di vincoli da far rispettare alla parola di opinione (per R1 AGGETTIVI)
  # JJ aggettivo, JJS aggettivo superlativo, JJR aggettivo comparativo

  for item in pos:  # scandisce i tag trovati dalla frase
    if item[1] in val:  # se il tag pos dela prima parola è presente nel vettore val
      agg = item[0]  # a agg assegno il termine (l'aggettivo)
      with open(Op) as myfile:  # apre il file op
        if agg in myfile.read():  # se l'aggettivo della frase è presente nel lessico di opinione positivo
          label = 'positive'  # label è positiva
      with open(On) as myfile:  # apre il file on
        if agg in myfile.read():  # se l'aggettivo della frase è presente nel lessico di opinione negativo
          label = 'negative'  # label è negativa
        MR = ['amod', 'advmod', 'rcmod']  # MR è l'array delle relazioni modifier [amod aggettivo riferito a un nome,
        # advmod aggettivo riferito a un avverbio, rcmod aggettivo riferito a un nome ma sottoforma di verbo
        # (es. il libro è stato scritto -> [libro,scritto])]
        # R11
        for items in depe:  # analizzando la i-esima tripla [('amod', 6, 4)]
          if items[0] in MR:  # se il tag della prima tripla è un MR [amod è in MR]
            opinion = items[2]  # allora mi salvo la posizione della parola di opinione dalla tripla [opinion=4]
            target = items[1]  # e mi salvo anche la posizione del target dalla tripla [target=6]
            # per la regola R11 se il target è un nome allora estrai la parola target [('player', 'NN') in pos[6-1]]
            if pos[target-1].__contains__('NN') or pos[target-1].__contains__('NNS'):  # verifica che il termine target è un nome [in questo caso lo è]
              o = tok[opinion-1]  # salvo la parola di opinione tok[3]=best
              # può essere commentato perchè la R1 non estrae parole di opinione
              t = tok[target-1]  # salvo la parola target tok[5]=player
              list_target.append(t)  # concateno alla lista dei target 'player'
              #O-->O-dep-->T

              # R12
              for items in depe:  # analizzando la i-esima tripla [('nsubj', 6, 1)]
                if items[0] == 'nsubj':  # se il tag della prima tripla è un nsubj [lo è]
                  if items[1] == target:  # verifica la dipendenza del target ovvero: [6 è uguale a target=6]
                    target = items[2]  # aggiorna il target con l'altro target collegato poichè nsubj collega 2 target [target=1]
                    if pos[target-1].__contains__('NN') or pos[target-1].__contains__('NNS'):  # verifica che il termine target è un nome [('iPod', 'NN') lo è]
                      t = tok[target-1]  # salvo la parola target tok[1-1]
                      list_target.append(t)  # concateno alla lista dei target 'iPod'
                      #O-->O-dep-->H<--T-dep<--T

  return set(list_target)  # restituisce la lista dei target estratti per ogni frase (alla seconda chiamata del metodo verranno concatenati altri target)


def R2(local_corenlp_path, input, file_target):  # in input la libreria, la frase da esaminare e il file dei target estratti

  toke, pos, depe = SC(local_corenlp_path, input)  # richiamo metodo per tokenizer tag pos e albero delle dipendenze
  # esempio di frase: iPod is the best mp3 player.
  # Tokeninze:  ['iPod', 'is', 'the', 'best', 'mp3', 'player', '.']
  # Part Of Speech:  [('iPod', 'NN'), ('is', 'VBZ'), ('the', 'DT'), ('best', 'JJS'), ('mp3', 'NN'), ('player', 'NN'), ('.', '.')]
  # Dependency Parse:  [('ROOT', 0, 6), ('nsubj', 6, 1), ('cop', 6, 2), ('det', 6, 3), ('amod', 6, 4), ('compound', 6, 5), ('punct', 6, 7)]Tokeninze:  ['this', 'camera', 'is', 'perfect', 'for', 'an', 'enthusiastic', 'amateur', 'photographer', '.']

  # stampa operazioni fatte
  print("Tokeninze: ", toke)
  print('\n')
  print("Part Of Speech: ", pos)
  print('\n')
  print("Dependency Parse: ", depe)
  print('\n')

  tok = np.array(toke)  # tok è l'array di singole parole in una frase
  list_opinion = []  # lista vuota che conterrà le parole di opinione

  val = ['NN', 'NNS']  # array di vincoli da far rispettare al target (per R2 SOSTANTIVI)
  # NN nome singolare, NNS nome plurale

  for item in pos:  # scandisce i tag trovati dalla frase
    if item[1] in val:  # se il tag pos dela prima parola è presente nel vettore val
      sost = item[0]  # a sost assegno il termine (il sostantivo)

      with open(file_target) as myfile:  # apre il file dei target estratti in precedenza
        if sost in myfile.read():  # se il sostantivo della frase è presente nel file dei target estratti in precedenza
          MR = ['amod', 'advmod', 'rcmod']  # MR è l'array delle relazioni modifier [amod aggettivo riferito a un nome,
          # advmod aggettivo riferito a un avverbio, rcmod aggettivo riferito a un nome ma sottoforma di verbo
          # (es. il libro è stato scritto -> [libro,scritto])]
          # R21
          for items in depe:  # analizzando la i-esima tripla [('amod', 6, 4)]
            if items[0] in MR:  # se il tag della prima tripla è un MR [amod è in MR]
              opinion = items[2]  # allora mi salvo la posizione della parola di opinione dalla tripla [opinion=4]
              target = items[1]  # e mi salvo anche la posizione del target dalla tripla [target=6]
              if pos[opinion - 1].__contains__('JJ') or pos[opinion - 1].__contains__('JJS') \
                      or pos[opinion - 1].__contains__('JJR'):
                # per la regola R21 se la parola di opinione è un aggettivo allora estrai la parola di opinione [('enthusiastic', 'JJ') in pos[7-1]]
                o = tok[opinion-1]  # salvo la parola di opinione tok[3]=best
                t = tok[target-1]  # salvo la parola target tok[5]=player
                # può essere commentato perchè la R2 non estrae target
                list_opinion.append(o)  # concateno alla lista delle parole di opinione 'best'
                # O-->O-dep-->T

              # R22
              for items in depe:  # analizzando la i-esima tripla [('nsubj', 6, 1)]
                if items[0] == 'nsubj':  # se il tag della prima tripla è un nsubj [lo è]
                  if items[1] == target:  # verifica la dipendenza del target ovvero: [6 è uguale a target=6]
                    target = items[2] # aggiorna il target con l'altro target collegato poichè nsubj collega 2 target [target=1]
                    if pos[opinion-1].__contains__('JJ') or pos[opinion-1].__contains__('JJS') \
                            or pos[opinion-1].__contains__('JJR'): # verifica che la parola di opinione è un aggettivo
                      o = tok[opinion - 1] # salvo la parola di opinione tok[3]=best
                      list_opinion.append(o) # concateno alla lista delle parole di opinione il termine
                      # O-->O-dep-->H<--T-dep<--T

  return set(list_opinion)  # restituisce la lista delle parole di opinione estratte per ogni frase
                            # (alla seconda chiamata del metodo verranno concatenati altre parole di opinione)


def R3(local_corenlp_path, input, file_target):  # in input la libreria, la frase da esaminare e il file dei target estratti

  toke, pos, depe = SC(local_corenlp_path, input)  # richiamo metodo per tokenizer tag pos e albero delle dipendenze
  # esempio di frase: it is small enough to fit easily in a coat pocket or purse.
  # Tokeninze:  ['it', 'is', 'small', 'enough', 'to', 'fit', 'easily', 'in', 'a', 'coat', 'pocket', 'or', 'purse', '.']
  # Part Of Speech:  [('it', 'PRP'), ('is', 'VBZ'), ('small', 'JJ'), ('enough', 'RB'), ('to', 'TO'), ('fit', 'VB'), ('easily', 'RB'), ('in', 'IN'), ('a', 'DT'), ('coat', 'NN'), ('pocket', 'NN'), ('or', 'CC'), ('purse', 'NN'), ('.', '.')]
  # Dependency Parse:  [('ROOT', 0, 3), ('nsubj', 3, 1), ('cop', 3, 2), ('advmod', 6, 4), ('mark', 6, 5), ('dep', 3, 6), ('advmod', 6, 7), ('case', 11, 8), ('det', 11, 9), ('compound', 11, 10), ('obl', 6, 11), ('cc', 13, 12), ('conj', 11, 13), ('punct', 3, 14)]

  # stampa operazioni fatte
  print("Tokeninze: ", toke)
  print('\n')
  print("Part Of Speech: ", pos)
  print('\n')
  print("Dependency Parse: ", depe)
  print('\n')

  tok = np.array(toke)  # tok è l'array delle singole parole di una frase
  list_target = []  # lista vuota che conterrà i target
  # R31
  for item in depe:  # analizzando la i-esima tripla [('conj', 11, 13)]
    if item[0] == 'conj':  # se il tag della prima tripla è un conj [lo è]
      n = tok[item[1]-1]  # tok[10]=n='pocket' che sarebbe il primo termine che partecipa alla congiunzione
      with open(file_target) as myfile:  # apre il file dei target estratti in precedenza
        if n in myfile.read():   # se il termine n fa parte di quella lista dei target estratti [non fa parte!!]
          t = item[2]  # allora mi salvo la posizione della seconda parola che partecipa alla congiunzione in t=13
          for item in pos:  # controllo se esiste il tag NN in pos
            if item[1].__contains__('NN') or item[1].__contains__('NNS'):
              target = tok[t-1]  # tok[12]=target=purse estraendo 'purse'
              list_target.append(target)  # aggiungo il termine target trovato alla lista dei target

  # R32
  for items in depe:  # fisso la 1° tripla e la controllo con le altre
    for items2 in depe:  # altre triple che scorrono
      if items[0] == items2[0]:  # se il tag della prima tripla è uguale al tag di una tripla che sto scorrendo
        if items[1] == items2[1]:  # verifica che le pos. delle parole di opinone delle due triple siano uguali: [es. [item=(mod,3,2) ed item2=(mod,3,6)]]
          target = items2[2]  # poichè 3=3, aggiorna il target con l'altro collegato da mod [target=6]
          if (pos[target-1].__contains__('NN') or pos[target-1].__contains__('NNS') or pos[target-1].__contains__('NNP'))\
                  and items != items2:  # verifica che il termine target è un nome e che le due triple siano diverse per evitare falsi
            t = tok[target-1]  # salvo la parola target tok[6-1]
            list_target.append(t)  # concateno alla lista il target trovato
            #Ti-->Ti-Dep-->H<--Tj-Dep<--Tj

  return set(list_target)  # restituisce la lista dei target estratti per ogni frase (alla seconda chiamata del metodo verranno concatenati altri target)


def R4(local_corenlp_path, input, file_opinion):  # in input la libreria, la frase da esaminare e il file dei target estratti

  toke, pos, depe = SC(local_corenlp_path, input) # richiamo metodo per tokenizer tag pos e albero delle dipendenze
  # esempio di frase: it is small enough to fit easily in a coat pocket or purse.
  # Tokeninze:  ['it', 'is', 'small', 'enough', 'to', 'fit', 'easily', 'in', 'a', 'coat', 'pocket', 'or', 'purse', '.']
  # Part Of Speech:  [('it', 'PRP'), ('is', 'VBZ'), ('small', 'JJ'), ('enough', 'RB'), ('to', 'TO'), ('fit', 'VB'), ('easily', 'RB'), ('in', 'IN'), ('a', 'DT'), ('coat', 'NN'), ('pocket', 'NN'), ('or', 'CC'), ('purse', 'NN'), ('.', '.')]
  # Dependency Parse:  [('ROOT', 0, 3), ('nsubj', 3, 1), ('cop', 3, 2), ('advmod', 6, 4), ('mark', 6, 5), ('dep', 3, 6), ('advmod', 6, 7), ('case', 11, 8), ('det', 11, 9), ('compound', 11, 10), ('obl', 6, 11), ('cc', 13, 12), ('conj', 11, 13), ('punct', 3, 14)]

  # stampa operazioni fatte
  print("Tokeninze: ", toke)
  print('\n')
  print("Part Of Speech: ", pos)
  print('\n')
  print("Dependency Parse: ", depe)
  print('\n')

  tok = np.array(toke)  # tok è l'array di singole parole in una frase
  list_opinion = []  # lista vuota che conterrà le parole di opinione
  # R41
  for item in depe:  # analizzando la i-esima tripla [('conj', 11, 13)]
    if item[0] == 'conj':  # se il tag della prima tripla è un conj [lo è]
      a = tok[item[1]-1]  # tok[10]=n='pocket' che sarebbe il primo termine che partecipa alla congiunzione
      with open(file_opinion) as myfile:  # apre il file delle parole di opinione estratte in precedenza
        if a in myfile.read():  # se il termine a fa parte di quella lista delle parole di opinione estratte [non fa parte!!]
          o = item[2]  # allora mi salvo la posizione della seconda parola che partecipa alla congiunzione in o=13
          for item in pos:  # controllo se esiste il tag JJ in pos
            if item[1].__contains__('JJ') or item[1].__contains__('JJS') \
                    or item[1].__contains__('JJR'):
              opinion = tok[o-1]  # tok[12]=target=purse estraendo 'purse'
              list_opinion.append(opinion)  # aggiungo la parola di opinione estratta alla lista delle parole di opinione
  # R42
  for items in depe:  # fisso la 1° tripla e la controllo con le altre
    for items2 in depe:  # altre triple che scorrono
      if items[0] == items2[0]:  # se il tag della prima tripla è uguale al tag di una tripla che sto scorrendo
        if items[2] == items2[2]:  # verifica che le pos. dei target delle due triple siano uguali: [es. [item=(mod,3,2) ed item2=(mod,3,6)]]
          opinion = items2[1]  # poichè 3=3, aggiorna la parola di opinione con l'altra collegata da mod [opinion=6]
          if (pos[opinion-1].__contains__('JJ') or pos[opinion-1].__contains__('JJS') or pos[opinion-1].__contains__('JJR'))\
                  and items != items2:  # verifica che il termine opinione è un aggettivo e che le due triple siano diverse per evitare falsi
            o = tok[opinion-1]  # salvo la parola di opinione tok[6-1]
            list_opinion.append(o)  # concateno alla lista il target trovato
            #Oi-->Oi-Dep-->H<--Oj-Dep<--Oj

  return set(list_opinion)  # restituisce la lista delle parole di opinione estratte per ogni frase
                            # (alla seconda chiamata del metodo verranno concatenate altre parole di opinione)

