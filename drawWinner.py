import re
import random
from datetime import datetime
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


def indexInList(key, listInput):
    if listInput == []:
        return -1
    for element in listInput:
        if element[0] == key:
            return listInput.index(element)
    return -1


def sortKey(elem):
    return elem[0]

def sortKey2(elem):
    return elem[1]


reddit = getReddit()


input = 'ervfni'


if len(input) > 8:
    submission = reddit.submission(url=input)
else:
    submission = reddit.submission(id=input)

print(50*'-')

print('Title: {}, score: {}, upvote ratio: {}, number of comments: {}'.format(submission.title,
                                                                              submission.score,
                                                                              submission.upvote_ratio,
                                                                              submission.num_comments))


print('time of draw: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

print(50*'-')

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
correctGuessCount = 0

submission.comments.replace_more(limit=None)
for top_level_comment in submission.comments:
    fac = 1
    if(check(top_level_comment.body, multiplyer)):
        fac = 2
        correctGuessCount = correctGuessCount + 1

    eNew = Entry(top_level_comment.author, top_level_comment.body, fac)

    if check(top_level_comment.body, keywords[0]):
        entriesGame1Single.append(eNew)
    elif check(top_level_comment.body, keywords[1]):
        entriesGame2Single.append(eNew)
    elif check(top_level_comment.body, keywords[2]):
        print('entry for both by ' + top_level_comment.author.name, end='')
        if random.random() < 0.5:
            print(', has been randomly assigned to Game1')
            entriesGame1Single.append(eNew)
        else:
            print(', has been randomly assigned to Game2')
            entriesGame2Single.append(eNew)
    else:
        entriesRejected.append(eNew)

random.shuffle(entriesGame1Single)
random.shuffle(entriesGame2Single)

for entry in entriesGame1Single:
    for i in range(entry.factor):
        entriesGame1Weighted.append(entry)

for entry in entriesGame2Single:
    for i in range(entry.factor):
        entriesGame2Weighted.append(entry)


random.shuffle(entriesGame1Weighted)
random.shuffle(entriesGame2Weighted)

print(50*'-')

print('Number of Entries for Game1: ' + str(len(entriesGame1Single)))
print('Number of Entries for Game2: ' + str(len(entriesGame2Single)))
print('Number of rejected Comments: ' + str(len(entriesRejected)))
print('Number of comments with correct guess ' + str(correctGuessCount))

print(50*'-')

winner1 = pickWinnerFrom(entriesGame1Weighted)
print('Winner for Game1 is ' + winner1.author.name)
winner2 = pickWinnerFrom(entriesGame2Weighted)
print('Winner for Game2 is ' + winner2.author.name)


print(50*'-')

participantsGame1 = []
for i in range(len(entriesGame1Weighted)):
    entry = entriesGame1Weighted[i]
    index = indexInList(entry.author.name, participantsGame1)
    if index == -1:
        participantsGame1.append([entry.author.name, i])
    else:
        tmp = participantsGame1.pop(index)
        tmp.append(i)
        participantsGame1.append(tmp)

participantsGame1.sort(key=sortKey)

participantsGame2 = []
for i in range(len(entriesGame2Weighted)):
    entry = entriesGame2Weighted[i]
    index = indexInList(entry.author.name, participantsGame2)
    if index == -1:
        participantsGame2.append([entry.author.name, i])
    else:
        tmp = participantsGame2.pop(index)
        tmp.append(i)
        participantsGame2.append(tmp)

participantsGame2.sort(key=sortKey)

print('Participant for Game1, sorted alphabetically:')
print(participantsGame1)
print('Participant for Game2, sorted alphabetically:')
print(participantsGame2)
participantsGame2.sort(key=sortKey2)
participantsGame1.sort(key=sortKey2)
print('Participant for Game1, sorted by lowest number:')
print(participantsGame1)
print('Participant for Game2, sorted by lowest number:')
print(participantsGame2)
print('Commenters who did not participate:')
namesRejected = ''
for entry in entriesRejected:
    namesRejected = namesRejected + ', ' + entry.author.name

namesRejected = namesRejected[2:len(namesRejected)]

print(namesRejected)
    