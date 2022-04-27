from pytube import YouTube


def downloadvideo(videolink, outputpath, itag=-1):
    yt = YouTube(videolink)
    print(yt.streams)  #look at needed itag
    if itag == -1:
        itag = input("Itag: ")
    stream = yt.streams.get_by_itag(itag)  #itag 315 = 4k (in this case)
    stream.download(output_path=outputpath)
    print(f"Finished downloading {yt.title}")
