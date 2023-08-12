from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os


def downloadlink(videolink, outputpath, itag=None, filename=''):
    yt = YouTube(videolink, on_progress_callback=on_progress)
    stream = yt.streams.get_by_itag(itag)  # look at needed itag, itag 315 = 4k (in this case)
    print(f'Downloading the {stream.type}: {yt.title}')
    if filename == '':
        file = stream.default_filename
        stream.download(output_path=outputpath)
    else:
        file = filename+stream.default_filename[stream.default_filename.index('.'):]
        stream.download(output_path=outputpath, filename=file)
    return file


def video_audio_merge(video, audio, final):
    videoclip = VideoFileClip(video)
    audioclip = AudioFileClip(audio)
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(final)


def show_options(videolink):
    yt = YouTube(videolink)
    print("VIDEO OPTIONS (mp4):\n")
    for option in reversed(yt.streams.order_by('resolution')):
        if option.is_progressive is False:
            if option.resolution != '1440p' and option.resolution != '2160p':
                if option.mime_type == "video/mp4" and option.video_codec[:4] != 'av01':
                    print(f"  Resolution:    {option.resolution:7}   Code: {option.itag}")
            else:
                if option.video_codec == 'vp9':
                    print(f"  Resolution:    {option.resolution:7}   Code: {option.itag}")
    print("\nAUDIO OPTIONS (mp3):\n")
    for option in reversed(yt.streams.order_by('abr')):
        if option.is_progressive is False:
            print(f"  Audio quality: {option.abr:7}   Code: {option.itag}")


def find_best_stream(yt, format):
    stream = None
    if format == 'video':
        for option in reversed(yt.streams.order_by('resolution')):
            if option.is_progressive is False:
                if option.resolution != '2160p' and option.resolution != '1440p':
                    if option.video_codec[:4] != 'av01':
                        stream = option
                        break
                else:
                    if option.video_codec == 'vp9':
                        stream = option
                        break
    if format == 'audio':
        for option in reversed(yt.streams.order_by('abr')):
            if option.is_progressive is False:
                stream = option
                break
    return stream

def downloadoptions(videolink, outputpath, itag=None, filename=''):
    yt = YouTube(videolink)
    video_stream = None
    audio_stream = None
    tempvideo_name = ''
    tempaudio_name = ''
    convertaud = ''
    convertvid = ''
    finalfile = ''
    video_conversion_needed = False
    still_selecting = False
    if itag is None:
        mode = int(input("Write 1 for best video+audio, 2 for best audio and 3 to choose: "))
        if mode == 1:
            itag = 'best video'
        elif mode == 2:
            itag = 'best audio'
        else:
            itag = 'select'
    if itag == 'best video':
        video_stream = find_best_stream(yt, 'video')
        audio_stream = find_best_stream(yt, 'audio')
    if itag == 'best audio':
        audio_stream = find_best_stream(yt, 'audio')
    if itag == 'select':
        still_selecting = True
        show_options(videolink)
        itag = int(input("\nWrite the code of the selected download and hit enter: "))
    if type(itag) == int:
        if yt.streams.get_by_itag(itag).type == 'audio':
            audio_stream = yt.streams.get_by_itag(itag)
        else:
            video_stream = yt.streams.get_by_itag(itag)
            if still_selecting is True:
                audio_needed = input("Do you also want the audio (y/n): ").lower()
                if audio_needed == 'y' or audio_needed == 'yes':
                    audio_stream = find_best_stream(yt, 'audio')
    if filename == '':
        filename = yt.streams.first().default_filename[:yt.streams.first().default_filename.index('.')]
    try:
        if video_stream is None:
            tempaudio_name = filename + ' temp audio'
            tempaudio = downloadlink(videolink, os.getcwd(), audio_stream.itag, tempaudio_name)
            finalfile = filename + '.mp3'
        else:
            if video_stream.resolution == '1440p' or video_stream.resolution == '2160p':
                video_conversion_needed = True
                tempvideo_name = filename + ' temp video'
            if audio_stream is None:
                if video_conversion_needed:
                    tempvideo = downloadlink(videolink, os.getcwd(), video_stream.itag, tempvideo_name)
                    finalfile = filename + '.mp4'
                else:
                    finalfile = downloadlink(videolink, os.getcwd(), video_stream.itag, filename)
            else:
                tempvideo_name = filename + ' temp video'
                tempvideo = downloadlink(videolink, os.getcwd(), video_stream.itag, tempvideo_name)
                tempaudio_name = filename + ' temp audio'
                tempaudio = downloadlink(videolink, os.getcwd(), audio_stream.itag, tempaudio_name)
                finalfile = filename + '.mp4'
        if tempaudio_name != '':
            if tempvideo_name == '':
                print("Converting the audio...")
                os.rename(tempaudio, finalfile)
            else:
                convertaud = filename + ' converted audio.mp3'
                print("Converting the audio...")
                os.rename(tempaudio, convertaud)
                if video_conversion_needed:
                    print("Converting the video...")
                    os.rename(tempvideo, tempvideo_name + '.mp4')
                    tempvideo = tempvideo_name + '.mp4'
                print("Merging video and audio...")
                video_audio_merge(tempvideo, convertaud, finalfile)
                os.remove(f'{os.getcwd()}\\{convertaud}')
                os.remove(f'{os.getcwd()}\\{tempvideo}')
        else:
            if video_conversion_needed:
                print("Converting the video...")
                os.rename(tempvideo, finalfile)
        os.rename(f'{os.getcwd()}\\{finalfile}', f'{outputpath}/{finalfile}')
    except:
        print("Something went wrong, please try again")
        if tempvideo_name != '':
            os.remove(f'{os.getcwd()}\\{tempvideo}')
        if tempaudio_name != '':
            os.remove(f'{os.getcwd()}\\{tempaudio}')
        if convertaud != '':
            os.remove(f'{os.getcwd()}\\{convertaud}')
        if convertvid != '':
            os.remove(f'{os.getcwd()}\\{convertvid}')
        if finalfile != '':
            os.remove(f'{os.getcwd()}\\{finalfile}')
    return yt


if __name__ == "__main__":
    videolink = "https://www.youtube.com/watch?v=OkMY1hRAlfc"
    outputpath = "C:/Users/sadee/Downloads"
    itag = 'best video'  # (optional) itag can be "best audio", "best video", "select" or certain numbers
    yt = downloadoptions(videolink, outputpath, itag)
    print(f'{yt.title} has finished downloading')
