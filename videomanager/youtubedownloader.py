from pytube import YouTube

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

videolink = "https://www.youtube.com/watch?v=5Ec47-RwFsM"
outputpath = "C:/Users/username/Downloads"
yt = YouTube(videolink)
print(yt.streams)  #look at needed itag
stream = yt.streams.get_by_itag(315)  #itag 315 = 4k (in this case)
stream.download(output_path=outputpath)
print(f"Finished downloading {yt.title}")
