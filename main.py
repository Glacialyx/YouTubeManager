import youtubemanager

videolink = "https://www.youtube.com/watch?v=LXb3EKWsInQ"
outputpath = "C:/Users/username/Downloads"
itag = 'best audio'  # (optional) itag can be "best audio", "best video", "select" or certain numbers (315 = 4k in this case)
yt = downloadoptions(videolink, outputpath, itag)
print(f'{yt.title} has finished downloading')
