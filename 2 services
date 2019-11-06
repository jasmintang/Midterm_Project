import os
import sys
from importlib import reload
from textblob import TextBlob
import pandas as pd
from collections import Counter
os.getcwd()
os.chdir('/Users/yamintang/Desktop/FE_595_Financial_Technology/team project/midterm')
reload(sys)
sys.getdefaultencoding()
f = 'test review.txt'
f_c = open(f)
fcs = f_c.read()
blob = TextBlob(fcs)
np = blob.noun_phrases


f_cs = []
for i in np:
    i = ''.join(i)
    blob = TextBlob(i)
    f_cs.append([blob.sentiment.polarity, i])
print(f_cs)

f_cs = pd.DataFrame(f_cs)
f_csr = f_cs.sort_values(by=0, ascending=False)


__they_data = dict()
for (i, j) in zip(f_csr[0], f_csr[1]):
    __they_data[j] = i
key=[]
for i in __they_data:
    key.append(i)
print("top_10_positive:")
for i in range(len(key)):
    if i > 9:
        break
    print(key[i])


print("\n\ntop_10_negative:")
for i in range(len(key)):
    if i > 9:
        break
    print(key[len(key)-i-1])


__my_data = []
for i in f_csr[1]:
    __my_data.append(i)
my_data = Counter(__my_data)

top_ten = my_data.most_common(10)
for i in top_ten:
    print(i)
print(top_ten)
