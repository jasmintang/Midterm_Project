import os
import sys
from importlib import reload
from typing import List, Any

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


def text(x):
    f_cs = []
    for i in x:
        i = ''.join(i)
        blob = TextBlob(i)
        f_cs.append([blob.sentiment.polarity, i])
    return f_cs
f_cs = pd.DataFrame(text(np))
f_cs = f_cs.sort_values(by=0, ascending=False)

# services
# positive characters
def positive(f_cs):
    key = []
    key2 = []
    __re_data = dict()
    for (i, b) in zip(f_cs[0], f_cs[1]):
        __re_data[b] = i
    for i in __re_data:
        key.append(i)
    for i in range(len(key)):
        if i > 9:
            break
        key2.append(key[i])
    return key2

# negative characters
def negative(f_cs):
    __re_data = dict()
    for (i, b) in zip(f_cs[0], f_cs[1]):
        __re_data[b] = i
    key_1 = []
    key_r = []
    for i in __re_data:
        key_1.append(i)
    for i in range(len(key_1)):
        if i > 9:
            break
        key_r.append(key_1[len(key_1)-i-1])
    return key_r


# top 10 common words
def common(f_cs):
    __my_data = []
    for i in f_cs[1]:
        __my_data.append(i)
        my_data = Counter(__my_data)
        top_ten = my_data.most_common(10)
    return top_ten
