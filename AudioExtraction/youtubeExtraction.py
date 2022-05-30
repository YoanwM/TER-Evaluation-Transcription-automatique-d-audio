import sys

from pytube import YouTube
import subprocess
import os
import re




def download_video(url:str):
    if url.startswith('https://www.youtube.com/watch?v=') :
        yt = yt = YouTube(url)
    else :
        raise SyntaxError("The link should start with https://www.youtube.com/watch?v=")
    return yt

def download_videos(filename_path:str = None, urls = []) :
    if filename_path != None :
        filein = open(filename_path, "r")
        urls = filein.readlines()
        filein.close()
    videos = []
    for url in urls :
        videos.append(download_video(url))
    return videos

def video_to_audio(video_name:str):

    extension = ".mp3"
    video_path = "./videos/"+video_name+"/"+video_name
    output =  "./videos/"+video_name+v.title+extension
    cmd = "ffmpeg -i \""+video_path+"\" -vn -ab 16k \""+output+"\""
    os.system(cmd)

    extension = ".wav"
    soundpath = output
    output_dir = "./audios/"+video_name
    sp = re.split("/", output_dir)
    output = "."
    for dirname in sp:
        if dirname != ".":
            output = output + "/"
            if not (os.listdir(output).__contains__(dirname)):
                output = output+dirname
                cmd = "mkdir \'"+output+"\'"
                os.system(cmd)
            else:
                output = output + dirname
    cmd = "ffmpeg -i \""+soundpath+"\" -acodec pcm_s16le -ac 1 -ar 16000 \"" + output+"/"+video_name+extension +"\""
    os.system(cmd)
    cmd = "rm \""+soundpath+"\""
    os.system(cmd)





if __name__ == '__main__':

    if sys.argv.__len__()>1 :
        urls = []
        for url in sys.argv[1:] :
            urls.append(url)
        videos = download_videos(urls)
    else :
        videos = download_videos(filename_path='./youtube_videos/urls')
    for v in videos :
        st_query = v.streams
        st_query.get_highest_resolution().download(output_path='./videos/'+v.title,filename=v.title)
        if not(os.listdir("./").__contains__("audios")):
            os.mkdir("./audios")
        if not(os.listdir("./audios").__contains__(v.title)):
            os.mkdir("./audios/"+v.title)
        video_to_audio(v.title)












        """
        vCaption = v.captions['a.fr']
        print(vCaption.download(title = v.title,srt=True))
        """

