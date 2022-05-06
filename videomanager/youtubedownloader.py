from pytube import YouTube
import os
'''
In pytube's cipher.py:
change var_regex at line 30 to this:
re.compile(r"^\$*\w+\W")
change lines 272-273 (in function_patterns) to this:
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
r'\([a-z]\s*=\s*([a-zA-Z0-9$]{2,3})(\[\d+\])?\([a-z]\)'
change line 288 to this:
nfunc=re.escape(function_match.group(1))),
'''


def converter_ffmpeg(input_file, output_file, input_path, audio_quality='160k'):
    os.chdir(input_path)
    conversion_command = f'ffmpeg -i "{input_file}" -crf 2 -b:a {audio_quality} "{output_file}"'
    os.system(conversion_command)



def video_audio_merge(video, audio, final):
    video_audio_merge_command = f'ffmpeg -i "{video}" -i "{audio}" -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy "{final}"'
    os.system(video_audio_merge_command)


def download(videolink, outputpath, itag=None, filename=''):
    yt = YouTube(videolink)
    print(yt.streams)  # look at needed itag
    stream = yt.streams.get_by_itag(itag)  # itag 315 = 4k (in this case)
    if filename == '':
        stream.download(output_path=outputpath)
    else:
        stream.download(output_path=outputpath, filename=filename+stream.default_filename[stream.default_filename.index('.'):])
    return yt


def downloadoptions(videolink, outputpath, itag=None, filename=''):
    yt = YouTube(videolink)
    print(f"{yt.title}")
    stream = ''
    if itag is None:
        bestie = int(input("Write 1 to download the best video+audio available or 2 to choose: "))
        if bestie == 1:
            itag = 'best'
        else:
            print("VIDEO OPTIONS:      Note: 1440p and 4k mp4 videos might not be supported on your device\n")
            for option in reversed(yt.streams.order_by('resolution')):
                if option.is_progressive is False:
                    if option.resolution != '1440p' and option.resolution != '2160p':
                        if option.mime_type == "video/mp4":
                            print(f"  Resolution:    {option.resolution:7}  Type: {'.mp4':6}  Code: {option.itag}")
                    else:
                        print(f"  Resolution:    {option.resolution:7}  Type: {option.default_filename[option.default_filename.index('.'):]:6}  Code: {option.itag}")
            print("\nAUDIO OPTIONS:\n")
            for option in reversed(yt.streams.order_by('abr')):
                if option.is_progressive is False:
                    print(f"  Audio quality: {option.abr:7}  Type: {'.mp3':6}  Code: {option.itag}")
            itag = int(input("\nWrite the code of the selected download and hit enter: "))
    both_vid_aud = 'y'
    if itag == 'best':
        for option in reversed(yt.streams.order_by('resolution')):
            if option.is_progressive is False:
                stream = option
                break
    else:
        stream = yt.streams.get_by_itag(itag)
        both_vid_aud = 'n'
        if stream.type == 'video':
            both_vid_aud = input("Do you also want the audio? (y/n): ")
    if filename == '':
        default_file = stream.default_filename
        filename = default_file[:default_file.index('.')]
    else:
        default_file = filename + stream.default_filename[stream.default_filename.index('.'):]
    final_file = default_file
    if both_vid_aud.lower() == 'n':
        if stream.type == 'audio':
            tempname = filename + ' temp'
            temp = tempname + default_file[default_file.index('.'):]
            download(videolink, os.getcwd(), stream.itag, tempname)
            final_file = filename + '.mp3'
            if temp[temp.index('.'):] != final_file[final_file.index('.'):]:
                converter_ffmpeg(temp, final_file, os.getcwd(), stream.abr[:stream.abr.index('b')])
                os.remove(f'{os.getcwd()}\\{temp}')
        elif stream.resolution == '1440p' or stream.resolution == '2160p':
            tempname = filename + ' temp'
            temp = tempname + default_file[default_file.index('.'):]
            download(videolink, os.getcwd(), stream.itag, tempname)
            final_file = filename + '.mp4'
            converter_ffmpeg(temp, final_file, os.getcwd(), stream.abr[:stream.abr.index('b')])
            os.remove(f'{os.getcwd()}\\{temp}')
        else:
            download(videolink, os.getcwd(), stream.itag, final_file)
        os.rename(f'{os.getcwd()}\\{final_file}', f'{outputpath}/{final_file}')
    else:
        tempvideoname = filename + ' temp video'
        tempvideo = tempvideoname + default_file[default_file.index('.'):]
        download(videolink, os.getcwd(), stream.itag, tempvideoname)
        converted_video = tempvideoname + ' converted.mp4'
        delete_tempvideo = True
        if tempvideo[tempvideo.index('.'):] != '.mp4' or stream.resolution == '1440p' or stream.resolution == '2160p':
            converter_ffmpeg(tempvideo, converted_video, os.getcwd())
            os.remove(f'{os.getcwd()}\\{tempvideo}')
            delete_tempvideo = False
        for option in reversed(yt.streams.order_by('abr')):
            if option.is_progressive is False:
                stream = option
                break
        default_file = stream.default_filename
        tempaudioname = filename + ' temp audio'
        tempaudio = tempaudioname + default_file[default_file.index('.'):]
        download(videolink, os.getcwd(), stream.itag, tempaudioname)
        converted_audio = tempaudioname + ' converted.mp3'
        delete_tempaudio = True
        if tempaudio[tempaudio.index('.'):] != '.mp3':
            converter_ffmpeg(tempaudio, converted_audio, os.getcwd())
            os.remove(f'{os.getcwd()}\\{tempaudio}')
            delete_tempaudio = False
        if not delete_tempaudio and not delete_tempvideo:
            video_audio_merge(converted_video, converted_audio, filename + '.mp4')
            os.remove(f'{os.getcwd()}\\{converted_video}')
            os.remove(f'{os.getcwd()}\\{converted_audio}')
        elif not delete_tempaudio and delete_tempvideo:
            video_audio_merge(tempvideo, converted_audio, filename + '.mp4')
            os.remove(f'{os.getcwd()}\\{tempvideo}')
            os.remove(f'{os.getcwd()}\\{converted_audio}')
        elif delete_tempaudio and not delete_tempvideo:
            video_audio_merge(converted_video, tempaudio, filename + '.mp4')
            os.remove(f'{os.getcwd()}\\{converted_video}')
            os.remove(f'{os.getcwd()}\\{tempaudio}')
        os.rename(f'{os.getcwd()}\\{final_file}', f'{outputpath}/{final_file}')
    return yt


videolink = "https://www.youtube.com/watch?v=Fmdb-KmlzD8"
outputpath = "C:/Users/sadee/Downloads"
itag = 299
yt = downloadoptions(videolink, outputpath)
print(f'{yt.title} has finished downloading')
