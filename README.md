# TER-Evaluation-Transcription-automatique-d-audio

Ce projet supervisé par Isabelle Ferrané, et réalisé par Dany Neang, Julian Villeneuve et Yoan Mollet à pour but l'extraction automatique de l'audio à partir d'urls de vidéo youtube (de préférence traitant de l'oenologie) afin d'en analyser la transcription via l'outil PATY developper par l'équipe SAMOVA de l'IRIT. 


## Extraction automatique 

Afin de réaliser la trancscription automatique, il faut lancer la ligne de commande suivante : 
`python3 ./AudioExtraction/youtubeExtraction.py [URLS]
`
- URLS est une option permettant de lister une ou plusieurs urls de vidéos youtube d'où la vidéos sera extraite 
- Si cette option n'est pas présente, l'extraction se fera à l'aide du fichier présent dans le fichier suivant : `./youtube_videos/urls`

L'extraction se fait en deux étapes : 
- Le téléchargement de(s) video(s) youtube dans le dossier `./videos/nom_de_la_video/la_video`
- L'extraction de l'audio en .wav de ces videos dans le dossier `./audios/nom_de_la_video/l'audio`

