import praw
import os
from collections import defaultdict
from unidecode import unidecode
from texttable import Texttable

username = 'TheLogicult'
password = 'login123'
clientid = '4aPG_jiHKVfhHg'
clientSecret =  'tUVV5R4MlAbwHlPQ4rDRCX1VQoA'

reddit = praw.Reddit(user_agent="RFL prediction extraction by u/TheLogicult", 
        client_id=clientid, client_secret=clientSecret,
        username=username, password=password)

url = "https://www.reddit.com/r/peloton/comments/i0l53o/rfl_20_strade_bianche_predictions_15_days_left/"
submission = reddit.submission(url=url)


d = defaultdict(int)
switcher = {
        0:20,
        1:18,
        2:16,
        3:14,
        4:12,
        5:10,
        6:10,
        7:10
        }

def addtodict(comment, d):
    counter = 0
    names = comment.split('\n')
    for i in range(len(names)):
        if len(names[i]) < 9:
            names[i] = ''
        else:
            names[i] = unidecode(names[i][9:].replace(' ', '')).lower()
    for name in names:
        if name:
            d[name] += switcher.get(counter, 0)
            counter += 1

for top_level_comment in submission.comments:
    addtodict(top_level_comment.body, d)


#print(d)


newD = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
newerD = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)[:20]}

#print(newD)
#print(newerD)

t = Texttable()
t.add_row(['Position', 'Cyclist', 'Points'])
position = 1
for i in newerD.keys():
    t.add_row([position, i, newerD[i]]) 
    position += 1


print(t.draw())
