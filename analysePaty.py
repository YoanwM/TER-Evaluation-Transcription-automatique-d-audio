# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 08:31:28 2022

@author: danyn
"""

import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
from matplotlib.ticker import PercentFormatter
import numpy as np
import json
import sys
#from matplotlib import rcParams
import subprocess as proc
import os
import shutil
#import IPython.display as aud
#import glob as g



#representation courbe de confiance des mots transcrits par paty 
#extraction des informations du fichier json de transcription par paty

#parameters
if len( sys.argv ) not in [5, 4, 3]:
    print( "\tusage: %s<option = 1> <transcrit.json> <audioname.wav> <seuil (0.0 to 0.9)>" % sys.argv[0] )
    print( "\tusage: %s<option = 2> <transcrit.json>" % sys.argv[0] )
    print( "\tusage: %s<option = 3> <transcrit.json> <Perplexity (5 to 50)>" % sys.argv[0] )
    sys.exit()

#note : no need to insert the full path directory of neither the audio or the transcription.

dossT = "patyTranscription/"
nomfichier = dossT + sys.argv[2]

extrait_range = 2 #en seconde

option = int(sys.argv[1])

###début :cette partie créée des structures de tableau remplies par les données du fichier json
#note : ne fonctionne qu'avec le format json de la transcription paty avec le model abdel option score confiance et temps
with open(nomfichier) as json_data:
    data_dict = json.load(json_data)
confidenceMoy = data_dict["confidence-score"]
words = data_dict["speakers"]
confSpk = [] #tab conf de chaque speak ex avec 2 spk : [[0.2, 0.3], [0.6, 0.9, 0.7]]
data = [] 
nomspk = [] #tab temp qui sert à créer confSpk

#parcours des dictionnaires dans words
for i in range(0, len(words)):
    #on mets en place un detecteur de locuteur dans nomspk
    spk = words[i]["speaker_id"]
    if spk not in nomspk:
        nomspk.append(spk)
        confSpk.append([])
    for j in range(len(words[i]["words"])):
        #on remplie les tableaux
        words[i]["words"][j]["speaker"] = words[i]["speaker_id"]
        data.append(words[i]["words"][j])
#construction du tableau confSpk
for i in range(0, len(words)):
    spk = words[i]["speaker_id"]
    for j in range(len(words[i]["words"])):
        confSpk[int(spk[-1]) - 1].append(words[i]["words"][j]["conf"])    

#remettre en ordre chronologique croissant par key "start" 
sortedtime = sorted(data, key=lambda d: d['start'])
listConf = []
listWord = []
listTime = []
abscisse = []
listT = []
#remplir les différents tableaux
for i in range(len(sortedtime)):
    listConf.append(sortedtime[i]["conf"])
    listWord.append(sortedtime[i]["word"])
    listTime.append( (sortedtime[i]["start"], sortedtime[i]["end"]) )
    listT.append(sortedtime[i]["start"])
    abscisse.append( str(listTime[i][0]) + "\n" + sortedtime[i]["speaker"] + ": " + str(listWord[i] ) )

npConf = np.array(listConf)
npWord = np.array(listWord)
npAbscisse = np.array(abscisse)
npTime = np.array(listTime)
npT = np.array(listT)
nbSpk = len(confSpk)

dimx = len(npConf) * 0.1
dimy = 10
###Fin :cette partie créée des structures de tableau remplies par les données du fichier json
    
print("nb word : " + str(len(npWord)))
print("nb spk : " + str(nbSpk))

#option 1
#graphique de score de confiance en fonction des mots transcrits
if option == 1:
    #construction des variable pour le nom, dossier du fichier audio 
    audioName = sys.argv[3]
    dossA = "audios/" + audioName[:-4]
    nomaudio = dossA + "/" + audioName
    print("nom audio = " + nomaudio)
    if len( sys.argv ) != 5:
        print( "\tusage: %s<option = 1> <transcrit.json> <audioname.wav> <seuil (0.0 to 0.9)>" % sys.argv[0] )
        sys.exit()
    seuil = float(sys.argv[4])
        
    plt.figure(figsize=(dimx, dimy))
    plt.title("score de confiance en fonction chronologique des mots trancrits par Paty")
    plt.plot(npConf)
    #définir les limites des axe
    plt.ylim(0,1.1)
    plt.xlim(1,len(npConf)+1)
    #mets les valeurs en abscisse en vertical poiur plus de lisibilité (90°) 
    plt.xticks(range(len(npWord)), npWord, rotation = 90)
    plt.axhline(y=seuil, xmin=0, xmax=1, color = "red", label ="seuil")
    plt.show()

  
#get all the word under seuil conf
    oddwords = [] #store les mots en dessous du seuil et les <unk>
    timers = [] #couple of time to get the timer extrait of oddword
    oddspeakers = []
    for element in sortedtime:
        if element["conf"] < seuil or element["word"] == "<unk>":
            oddwords.append("unk") if element["word"] == "<unk>" else oddwords.append(element["word"])
            start = round(element["start"] - extrait_range, 1) if element["start"] - extrait_range > 0 else 0
            end = round(element["end"] + extrait_range, 1)
            #add 2s of duration at debut and fin
            timers.append((start, end))
            oddspeakers.append( element["speaker"])
    #create all oddaudio
    oddw_folder = "odd_words"
    if not(os.path.exists(oddw_folder)): #creation du dossier
        os.mkdir("./" + oddw_folder)
    tempdest = "odd_words_" + audioName[:-4] #:-4 enleve l'extension du fichier en string
    tempdir = oddw_folder + "/" + tempdest
    if (os.path.exists(tempdir)): #supprime le dossier si déjà existant
        shutil.rmtree(tempdir) #remove in order to clean before
    os.mkdir(tempdir)
    #create temp file for each audio 
    #name struct : [start]_oddword_[end]speaker.mp3
    print("running ffmpeg cmd...")
    for index, (start, end)  in enumerate(timers):
        name = oddw_folder + "/" + tempdest + "/" + "[" + str(start) + "]" + oddwords[index] + "[" + str(end) + "]" + oddspeakers[index] + ".wav"
        #print(name)
        length = round(end - start,1)
        cmd = "ffmpeg -ss " + str(start) + " -t " + str(length) + " -i " +  "\"" + nomaudio + "\"" + " \"" + name + "\""
        print(cmd)
        if proc.run(cmd, shell = True).returncode != 0:
            print("ffmpeg fail")
    print("...done \n check audios samples in folder " + tempdir)

   
#option 2
#histogramme de comparaison des speakers avec leurs scores de confiaces respectifs
#affichage histogramme tout speakers confondus (nb de score en tranche seuil de 0.1)
if option == 2:
    if len(sys.argv) != 3:
        print( "\tusage: %s<option = 2> <transcrit.json>" % sys.argv[0] )
        sys.exit()
        
    plt.hist(npConf, range= (0, 1), bins = 10, edgecolor = 'black')
    plt.title("Répartition des nombres de score de confiance entre différents seuils")
    histox = 15
    histoy = 10
    plt.xlim(0,1)
    abx = np.arange(0, 1.1, 0.1)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(npConf)))
    plt.xticks(abx)
    plt.show()
    
    #2ème histogramme
    #Répartition du nombre de score de confiance des mots dans différent intervalle de chaque speaker
    nbSpk = len(confSpk)
    plt.figure(figsize=(nbSpk * 2, dimy / 2 ))
    plt.hist(confSpk, range = (0, 1), label = ["Speaker " + str(i) for i in range(nbSpk)])
    plt.legend(loc='upper left')
    plt.title("Répartition des nombres de score de confiance des speakers entre différents seuils en pourcentage")
    plt.xlim(0,1)
    abx = np.arange(0, 1.1, 0.1)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(npConf)))
    plt.xticks(abx)
    plt.show()
    
    #pie
    #taux de parole (nombre de mot dit) de chaque speaker
    #tabword_speaker = [nb_word_spk0, nb_word_spk1, ...]
    tabword_speaker = [len(confSpk[i]) for i in range(nbSpk)]
    
    plt.figure(figsize = (8, 8))
    plt.pie(tabword_speaker, labels = ["Speaker " + str(i) for i in range(nbSpk)],
               autopct = lambda x: str(round(x, 2)) + '%',
               )
    plt.title("Répartition du taux de parole entre les différents speakers")
    plt.legend(loc='upper left')
    
    #debit de parole en mots par minutes
    #debit de "parole" de chaque speaker: mots/minute (moyen : 150mots/min pour être bien audible) 
    #tabDebit : [(nbWord spk1, time total spk1),..., (nbWord spk n, time spk n) ...]
    moyenDebit = 200
    tabDebit = [round((len(words[i]["words"])) / (words[i]["end"] - words[i]["start"]) * 60) for i in range(nbSpk)]
    spk = ["spk" + str(i) for i in range(nbSpk)]
    fig = plt.figure(figsize=(nbSpk, 5))
    ax = fig.add_axes([0,0,1,1])
    ax.bar(spk, tabDebit)
    plt.axhline(y=200, color = "green", label ="debit moyen général")
    plt.legend()
    plt.title("Debit de parole en mots par minutes de chaque speakers")
    ax.set_ylabel("Mots/minutes")
    plt.show()

#option 3
#word embedding représenation
if option == 3:
    if len(sys.argv) != 4:
        print( "\tusage: %s<option = 3> <transcrit.json> <nb perplexity>" % sys.argv[0] )
        sys.exit()
    import spacy
    from sklearn.manifold import TSNE
    
    nbPerp = int(sys.argv[3])
    
    #╣you can add more if trouble
    dictcolor = {"NOUN": "royalblue",
             "ADJ" : "red",
             "ADV" : "green",
             "VERB": "pink",
             "PROPN":"lightcyan",
             "NUM": "tan",
             "ADP":"maroon",
             "AUX": "pink",
             "CCONJ": "black",
             "PRON": "yellow",
             "X" :"cyan",
             "PUNCT":"blue"}
    
    #building raw text
    def buildText(tabWord):
        text = ""
        for word in tabWord:
            if word != "<unk>":
                if word[-1] != "'":
                    text += word + " "
                else:
                    text += word
        return text
    text = buildText(npWord)
    #python -m spacy download fr_core_news_sm
    #model français
    nlp = spacy.load("fr_core_news_lg")
    rawText = nlp(text)
    stemText = ""
    print("\n texte brut :\n", rawText)
    
    #traitement
    #remove stop_list + stemming (core word)
    stemText = nlp(buildText([str(token.lemma_) for token in rawText if not(token.is_stop or token.is_punct)]))
    stemText = nlp(buildText([str(token.lemma_) for token in stemText if not(token.is_stop or token.is_punct)]))
    print("\n texte posttraitement :\n", stemText, "\n")  
    
    #each token has a vector of word embedding
    word_emb = [word.vector for word in stemText]
    
    #representation des words embeddings 2d (all token)
    tsne2d = TSNE(n_components = 2, perplexity = nbPerp, random_state = 0)
    tsne_word_emb2d = tsne2d.fit_transform(word_emb)
    x = tsne_word_emb2d[:,0]
    y = tsne_word_emb2d[:,1]
    plt.figure(figsize=(dimy, dimy))
    for i, token in enumerate(stemText):
        plt.scatter(x[i], y[i], c = dictcolor[token.pos_], label = token.pos_)
        plt.text(x[i], (y[i]), str(token))
        
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())    
    plt.title("Répresentation des words embeddings avec réduction de dimension par TNSE")
    plt.show()
    
    #représentation des words embeddings 2d (nom token)
    plt.figure(figsize=(dimy, dimy))
    for i, token in enumerate(stemText):
        if token.pos_ == "NOUN":
            plt.scatter(x[i], y[i], c = dictcolor[token.pos_], label = token.pos_)
            plt.text(x[i], (y[i]), str(token))
            
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())    
    plt.title("Répresentation des words embeddings des NOMS avec réduction de dimension par TNSE")
    plt.show()
    
    #représentation des words embeddings 2d (verbe token)
    plt.figure(figsize=(dimy, dimy))
    for i, token in enumerate(stemText):
        if token.pos_ == "VERB":
            plt.scatter(x[i], y[i], c = dictcolor[token.pos_], label = token.pos_)
            plt.text(x[i], (y[i]), str(token))
            
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())    
    plt.title("Répresentation des words embeddings des VERBS avec réduction de dimension par TNSE")
    plt.show()
    
    #représentation des words embeddings 2d (adj token)
    plt.figure(figsize=(dimy, dimy))
    for i, token in enumerate(stemText):
        if token.pos_ == "ADJ":
            plt.scatter(x[i], y[i], c = dictcolor[token.pos_], label = token.pos_)
            plt.text(x[i], (y[i]), str(token))
            
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())    
    plt.title("Répresentation des words embeddings des ADJS avec réduction de dimension par TNSE")
    plt.show()
    
