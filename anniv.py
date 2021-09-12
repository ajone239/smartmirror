from bs4 import BeautifulSoup as bs
import requests
import datetime
import re
import os

r = r';'
re.compile(r)

def fix_unicode_issues(st):
    newst = []
    for c in st:
        if ord(c) == 177:
            c = '+-'
        elif ord(c) == 181:
            c = 'u'
        elif ord(c) > 128:
            c = ''
        newst.append(c)
    st = ''.join(newst)
    return st

def dailyjesus():
    try:
        data = requests.get('https://www.biblestudytools.com/bible-verse-of-the-day/')
    except:
        return 'Turn on wifi'

    soup = bs(data.text, 'html.parser')

    quote = soup.find('div',attrs = {'class','panel bst-panel carousel slide'})

    verse = quote.find('p', attrs = {'class', 'scripture'})

    title = str(fix_unicode_issues(verse.a.text)).strip()
    body = str(fix_unicode_issues(verse.span.text)).strip()
    body = re.sub(r'^\d','',body)

    return '%s: %s' % (title,body)

def dailyquote():
    try:
        response = requests.get('http://73.113.23.66/daily.txt').text
    except:
        return 'There\'s an error with the website.'

    lines = []
    hold = ''

    for char in response:
        hold += char
        if char == '\n':
            line = hold
            hold = ''
            if line and re.search(r,line):
                line = line.split(';')
                lines.append(line)

    today = str(datetime.datetime.now())
    today = today.split(' ')[0]

    for line in lines:
        if line[0] == today:
            return line[1] + ' -Austin Jones\n'

    return 'Something unforseen has happened, however I love you.'

def timesince():

    ann = [2017,5,27]
    mtd = [31,28,31,30,31,30,31,30,31,30,31]
    dateout = ['year','month','day']

    today = str(datetime.datetime.now())
    today = today.split(' ')[0]
    today = today.split('-')


    since = []

    for i in range(3):
        dif = int(today[i]) - ann[i]
        since.append(dif)

    if since[1] < 0:
        since[0]-=1
        since[1] = 12 + since[1]

    if since[2] < 0:
        if since[1] == 0:
            since[1] = 11
            since[0]-=1
        else:
            since[1]-=1
        if (int(today[0]) % 4) == 0:
            mtd[1]+=1
        since[2] = mtd[int(today[1])] + since[2]

    for i in range(3):
        if since[i] > 1:
           dateout[i] = dateout[i]+ 's'

    return "Dating your nerd for:\n%s %s, %s %s, and %s %s" % (since[0], dateout[0], since[1],dateout[1], since[2],dateout[2])

if __name__ == "__main__":
    print(timesince())
    print(dailyquote())
    print(dailyjesus())
