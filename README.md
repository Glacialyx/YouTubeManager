# VIDEOMANAGER
Repository to download and manage videos.
In pytube's cipher.py:
change var_regex at line 30 to this:
re.compile(r"^\$*\w+\W")
change lines 272-273 (in function_patterns) to this:
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
r'\([a-z]\s*=\s*([a-zA-Z0-9$]{2,3})(\[\d+\])?\([a-z]\)'
change line 288 to this:
nfunc=re.escape(function_match.group(1))),
