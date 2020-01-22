import re
import random
import praw
from config import getReddit


class Entry:
  def __init__(self, author, body, factor):
    self.author = author
    self.body = body
    self.factor = factor



def check(text, keys):
    for key in keys:
        if re.search(key, text, re.I):
            return True
    return False

def pickWinnerFrom(entries):
    winnerIndex = random.randint(0, len(entries)-1)
    print('Winning number is ' + str(winnerIndex))
    return entries[winnerIndex]

reddit = getReddit()


input = 'ervfni'


if len(input)> 8:
    submission = reddit.submission(url=input)
else:
    submission = reddit.submission(id=input)

print('Title: {}, score: {}, upvote ratio: {}, number of comments: {}'.format(submission.title,
                                                                           submission.score,
                                                                           submission.upvote_ratio,
                                                                           submission.num_comments))

entriesGame1Single = []
entriesGame2Single = []
entriesGame1Weighted = []
entriesGame2Weighted = []
entriesRejected = []

keywordsGame1 = ['satellite', 'reign', 'sattelite', 'satelite']
keywordsGame2 = ['hack', 'hacknet']
keywordsUniversal = ['either', 'any game', 'both', 'no preference']


keywords = [keywordsGame1, keywordsGame2, keywordsUniversal]
multiplyer = ['purple']

submission.comments.replace_more(limit=None)
for top_level_comment in submission.comments:
    fac = 2
    if(check(top_level_comment.body, multiplyer)):
        fac = 4
    if check(top_level_comment.body, keywords[0]):
        eNew = Entry(top_level_comment.author, top_level_comment.body, fac)
        entriesGame1Single.append(eNew)
    elif check(top_level_comment.body, keywords[1]):
        eNew = Entry(top_level_comment.author, top_level_comment.body, fac)
        entriesGame2Single.append(eNew)
    elif check(top_level_comment.body, keywords[2]):
        eNew = Entry(top_level_comment.author, top_level_comment.body, int(fac/2))
        print('entry for both by ' + top_level_comment.author.name)
        if random.random() < 0.5:
            print('assigned to Game1')
            entriesGame1Single.append(eNew)
        else:
            print('assigned to Game2')
            entriesGame2Single.append(eNew)
    else:
        eNew = Entry(top_level_comment.author, top_level_comment.body, 0)
        entriesRejected.append(eNew)


for entry in entriesGame1Single:
    for i in range(entry.factor):
        entriesGame1Weighted.append(entry)

for entry in entriesGame2Single:
    for i in range(entry.factor):
        entriesGame2Weighted.append(entry)



print('Number of Entries for Game1: ' + str(len(entriesGame1Single)))
print('Number of Entries for Game2: ' + str(len(entriesGame2Single)))
print('Number of rejected Comments: ' + str(len(entriesRejected)))

winner1 = pickWinnerFrom(entriesGame1Single)
print(winner1.author.name)
winner2 = pickWinnerFrom(entriesGame2Single)
print(winner2.author.name)
