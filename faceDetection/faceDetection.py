

"""
Before using this python script, be sure to be in a correct environment
You can create one like this :
$ conda create -n pyannote python=3.6 anaconda
$ source activate pyannote

Then, install pyannote-video and its dependencies:

$ pip install pyannote-video

Finally, download sample video and dlib models:

$ git clone https://github.com/pyannote/pyannote-data.git
$ git clone https://github.com/davisking/dlib-models.git
$ bunzip2 dlib-models/dlib_face_recognition_resnet_model_v1.dat.bz2
$ bunzip2 dlib-models/shape_predictor_68_face_landmarks.dat.bz2


To run this script, you need to be in the main directory using :
$ python3 ./faceDetection/faceDetection.py

"""
import os
from pyannote.core.json import load_from
from pyannote.core.notebook import repr_timeline
import cv2

if __name__ == '__main__':

    titles = os.listdir('./faceDetection/datas')
    for title in titles :

        # Here we make a path to the different files to make and use
        dir_path = "./faceDetection/datas/" + title + "/"
        shots_extension = ".shots.json"
        track_extension = ".track.txt"
        video_track_extension = ".track.mp4"
        landmark_extension = ".landmarks.txt"
        embedding_extension = ".embedding.txt"

        video_path = "\"./videos/" + title + "/" + title + ".mp4\""

        shots_path = dir_path + title + shots_extension + "\""
        track_path = dir_path + title + track_extension
        video_track_path = dir_path + title + video_track_extension
        landmark_path = dir_path + title + landmark_extension
        embedding_path = dir_path + title + embedding_extension

        # In this part we make the shot segmentation

        os.system("pyannote-structure.py shot --verbose \$video_path \$shots_path")
        shots = load_from(shots_path)
