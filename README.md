# TER-Evaluation-Transcription-automatique-d-audio

Ce projet supervisé par Isabelle Ferrané, et réalisé par Dany Neang, Julian Villeneuve et Yoan Mollet à pour but l'extraction automatique de l'audio à partir d'urls de vidéo youtube (de préférence traitant de l'oenologie) afin d'en analyser la transcription via l'outil PATY developper par l'équipe SAMOVA de l'IRIT. 


## Extraction automatique 
Pour commencer, il faut utiliser le bon environement :

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

La detection de visages dans les vidéos se fait à l'aide de pyannote-vidéo.
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

