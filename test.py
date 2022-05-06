# from inputimeout import inputimeout, TimeoutOccurred
# from googletrans import Translator

# try:
#     something = inputimeout(prompt='번역해줌 : ', timeout=3)
#     t = Translator()
#     a = t.translate(something, src="en", dest="ko")
#     print(a.text)
# except TimeoutOccurred:
#     print("시간초과!!")

import googletrans
from googletrans import Translator
 
d = googletrans.LANGUAGES
 
text1 = "안녕하세요"
t = Translator()

for i in d:
        
    trans1 = t.translate(text1, src='ko', dest=i)
    print(f"{d[i]} 의 인삿말 : ", trans1.text)
