# TER-Evaluation-Transcription-automatique-d-audio

Ce projet supervisé par Isabelle Ferrané, et réalisé par Dany Neang, Julian Villeneuve et Yoan Mollet à pour but l'extraction automatique de l'audio à partir d'urls de vidéo youtube (de préférence traitant de l'oenologie) afin d'en analyser la transcription via l'outil PATY developper par l'équipe SAMOVA de l'IRIT. 


## Extraction automatique 

Afin de réaliser la trancscription automatique, il faut lancer la ligne de commande suivante : 
```$ python3 ./AudioExtraction/youtubeExtraction.py [URLS]
```
- URLS est une option permettant de lister une ou plusieurs urls de vidéos youtube d'où la vidéos sera extraite 
- Si cette option n'est pas présente, l'extraction se fera à l'aide du fichier présent dans le fichier suivant : `./youtube_videos/urls`

L'extraction se fait en deux étapes : 
- Le téléchargement de(s) video(s) youtube dans le dossier `./videos/nom_de_la_video/la_video`
- L'extraction de l'audio en .wav de ces videos dans le dossier `./audios/nom_de_la_video/l'audio`

## PyBK

PyBK est un système de diarization sur une liste d'audios donnée, développé par Jose PATINO. Ici, on cherchera principalement à comparer PyBK et PATY quant à la
segmentation et au clustering des locuteurs dans diverses vidéos.

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


