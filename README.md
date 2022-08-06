# TER-Evaluation-Transcription-automatique-d-audio

Ce projet supervisé par Isabelle Ferrané, et réalisé par Dany Neang, Julian Villeneuve et Yoan Mollet à pour but l'extraction automatique de l'audio à partir d'urls de vidéo youtube (de préférence traitant de l'oenologie) afin d'en analyser la transcription via l'outil PATY developper par l'équipe SAMOVA de l'IRIT. 


## Extraction automatique 
Nous utilisons essentiellement anaconda pour gérer notre environnement de travail.
Pour commencer, il faut utiliser le bon environement:

```
$ conda create -n extraction python=3.6
$ source activate pyBK
$ conda install pytube
```


Afin de réaliser la transcription automatique, il faut lancer la ligne de commande suivante : 
```
$ python3 ./AudioExtraction/youtubeExtraction.py [URLS]
```
- URLS est une option permettant de lister une ou plusieurs urls de vidéos youtube d'où la vidéos sera extraite. Pour rajouter une vidéo à la liste, il suffit de rajouter son url youtube à la liste et ensuite de lancer le script.
- Si cette option n'est pas présente, l'extraction se fera à l'aide du fichier présent dans le fichier suivant : `./youtube_videos/urls`

L'extraction se fait en deux étapes : 
- Le téléchargement de(s) video(s) youtube dans le dossier `./videos/nom_de_la_video/la_video`
- L'extraction de l'audio en .wav de ces videos dans le dossier `./audios/nom_de_la_video/l'audio` 
- 
## Transcription automatique audio avec PATY

### Utilisation de PATY

Cette partie se base sur les résultats des transcriptions de nos audios déjà préparés avec la rubrique précédente.
Nous vous invitons à utiliser paty, développé par l'équipe SAMOVA, grâce à sa démo : https://paty.irit.fr/demo/.
PATY est un outil de transcription automatique de parole proposant ses services en se basant sur plusieurs models qui ont servi à son apprentissage.

Nous avons choisi le **model "abdel"**, un model avec le plus grand vocabulaire pour notre projet.

Pour utiliser notre outil d'analyse de la transcription il vous faudra utiliser le **format de transcription avec json** ainsi que les options ***score de confiance et temps.***
Une fois les transcriptions obtenues et placées manuellement dans le **dossier "/patyTranscription"**, nous pouvons entamer les analyses.

### Analyse des transcriptions
#### Environnement et librairies
Notre programme python "analysePaty.py" utilise certaines librairies : spacy (et son vocabulaire fr lg), matplotlib, json, sys, subprocess, os, shutil, glob et sklearn. 
il vous fraudra les installer dans votre environnement voici les lignes d'installation avec anaconda (certaines sont déjà installées par défaut) :

```
$ conda install -c conda-forge spacy
$ python -m spacy download fr_core_news_lg --user
$ conda install -c conda-forge matplotlib
$ conda install numpy
$ conda install -c jmcmurray json
$ conda install -c conda-forge r-sys
& conda install -c omnia subprocess32
$ conda install -c jmcmurray os
$ conda install -c conda-forge pytest-shutil
$ conda install -c conda-forge glob2
$ conda install -c anaconda scikit-learn
& conda install -c conda-forge ffmpeg   
```

#### Exécution de l'analyse
Il ne reste qu'à exécuter le programme analysePaty.py. Il est conseillé d'utiliser Spyder pour des résultats plus lisibles.
Il ne faut pas inserer tout le path directory du fichier de transcription et du fichier audio (trancription.json myaudio.wav suffit). Format d'exécution en fonction de 3 options possibles:

####Option 1 : Analyse du score de confiance des mots 
Format : python3 <option = 1> <transcrition.json> <audioname.wav> <seuil (0.0 to 0.9)>.

Montre un graphique de score de confiance en fonction des mots transcrits. 
Prépare des extraits à écouter (dans le dossier "odd_words") qui se focus sur les mots dont le score de confiance est en dessous du seuil.

####Option 2 : Analyse du score de confiance des locuteurs identifiés
Format : python3 analysePaty.py <option = 3> <transcrition.json>

Montre un histogramme de comparaison des speakers avec leurs scores de confiances respectifs.
Affichage histogramme tous speakers confondus (nb de score en tranche seuil de 0.1).
Histogramme : Répartition du nombre de score de confiance des mots dans différents intervalles de chaque speaker.
Pie : Taux de parole (nombre de mot dit) de chaque speaker.
Histogramme de débit de parole.

####Option 3 : Word embedding 
Format : python3 analysePaty.py <option = 3> <transcrit.json> <nbPerpl (5 to 30)>
Représentation 2d avec T-NSE des words embedding des mots transcrits.


## Diarization

Ici, on cherchera principalement à comparer PyBK et PyAnnote quant à la segmentation et au clustering des locuteurs dans diverses vidéos.

### PyBK

PyBK est un système de diarization sur une liste d'audios donnée, développé par Jose PATINO.

Pour l'utiliser, il faut tout d'abord avoir les bons outils et préparer le bon environnement. Si vous utilisez conda, les commandes suivantes devraient suffire :

```
$ conda create -n pyBK python=3.6
$ source activate pyBK
$ conda install numpy
$ conda install -c conda-forge librosa
$ pip install webrtcvad
$ git clone https://github.com/josepatino/pyBK.git
```

Une fois dans le bon environnement, il faut utiliser les commandes suivantes pour procéder à l'analyse des fichiers audios qui ont été
déposé dans le dossier /audio :

```
$ cd pyBK
$ python main.py
```

Il suffit d'ajouter des fichiers au format .waw dans le dossier /audio pour les analyser, le résultat de l'analyse sera automatiquement retranscrite dans le fichier
texte resultats.txt. On peut déjà consulter celui qui a été push dans la version actuelle analysant les vidéos qui ont été données, la liste étant consultable
dans le dossier /videos (certains ont été retirés du dossier pyBK/audio faute de taille).

### PyAnnote [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1oBjSFLJx7uAwPvKcHa_BhcfDHQsfqXLU?usp=sharing)

PyAnnote audio est, comme PyBK, un outil open-source de diarization cette fois développé par Hervé BREDIN de l'équipe SAMOVA de l'IRIT.

Tout est indiqué dans [ce notebook](https://colab.research.google.com/drive/1oBjSFLJx7uAwPvKcHa_BhcfDHQsfqXLU?usp=sharing) sur Google Colab.
***Aucune cellule donnant des graphes ne doit être lancée***, cela ne sert à rien et la diarization prend beaucoup de temps (facilement 5 fois plus que la durée de la vidéo).

Pour faire de la diarization sur vos propres vidéos afin d'essayer par vous même, il suffit tout d'abord de lancer la cellule d'installation, de lancer ensuite 
la cellule de la rubrique "Téléchargement de vos vidéos" qui vous permettra de choisir votre fichier audio au format .wav, puis de lancer
la dernière cellule du notebook appelée "Diarization de votre vidéo".


## Detection de visages

### Avec pyannote : 

La detection de visages dans les vidéos se fait à l'aide de pyannote-vidéo ou opencv (moins bien).
Pour l'utiliser, il faut d'abord se créer un bon environement (copier depuis pyannote-vidéo):

```bash
$ conda create -n pyannote python=3.6 anaconda
$ source activate pyannote
```

Ensuite on installe pyannote-vidéo et ses dépendances :

```bash
$ pip install pyannote-video
```

```bash
$ git clone https://github.com/pyannote/pyannote-data.git
$ git clone https://github.com/davisking/dlib-models.git
$ bunzip2 dlib-models/dlib_face_recognition_resnet_model_v1.dat.bz2
$ bunzip2 dlib-models/shape_predictor_68_face_landmarks.dat.bz2
```

Ensuite il faut lancer un des notebook situé dans le dossier `faceDetection` et se laisser guider.

### Avec openCV (moins utile et performant) :

Il faut commencer par se créer un bon environnement :

```bash
$ conda create -n faceDetection python=3.9 anaconda
$ source activate faceDetection
```

Ensuite on installe opencv :

```bash
$ pip install opencv-python
```

Puis lancer le notebook et se laisser guider. 
Les vidéos se chargeront directement dans le dossier courant.

## Detection d'objet

La detection d'objet dans les vidéos se fait à l'aide de d'openCV et Yolo.
Pour l'utiliser, il faut d'abord se créer un bon environement :

```bash
$ conda create -n objectDetection python=3.9 anaconda
$ source activate objectDetection
```

Ensuite on installe opencv :

```bash
$ pip install opencv-python
```
pour finir, téléchargez les yolo weights:

```bash
$ wget https://pjreddie.com/media/files/yolov3.weights
```

Pour utiliser la détection d'objet, il faut se placer dans le dossier `objectDetection`.

Ensuite, il faut lancer le script python : 
```bash
$ python3 ./objectDetection --title Titre_de_la_video [--frame_drop frame_drop] [--confidence_min confidence_min]
```

L'argument *frame_drop* est optionnel (initialisé à 50 par défaut), et sert à traiter une images toutes les *frame\_drop*  images. 
L'argument *confidence_min* est optionnel (initialisé à 0.5 par défaut), et représente la confiance minimum pour afficher les boites sur les images.

Ce script télécharge d'abord les images dans le dossier `titre_de_la_video/Images`, enregistre les images traitées dans `titre_de_la_video/Results` et crée un fichier `titre_de_la_video.txt` contenant les informations sur les boites avec des lignes de la forme : `numéro_de_l'image label indice_de_confiance`.




