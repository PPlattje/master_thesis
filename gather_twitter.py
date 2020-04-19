#script to gather 1000 tweets for each bad word in our dictionary
import tweepy as tw
import re
import time

#twitter API credentials
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
idlist = []

#create file: only when not continuing a previous run.
#with open('badwordtweetsxxl.txt', 'w') as f:
#    print('creating file')

with open('dictionaries/wiegand_e_075', 'r') as f:
    regex = re.compile(r".+?(?=_)")
    lines = f.readlines()
    wordlist = []
    for line in lines:
        word = re.match(regex, line)[0]
        if word not in wordlist:
            wordlist.append(word) 
wordnum = 0
contin = 0
while len(wordlist) > 0:
    wordnum += 1
    word = wordlist.pop()
    if contin == 1:
        query = word + ' -filter:retweets'
        tweets = tw.Cursor(api.search, q=query, lang='en', tweet_mode='extended').items()
        with open('badwordtweetsxxl.txt', 'a') as f:
            num = 0
            for item in tweets:
                if item.id not in idlist:
                    print(item.full_text, file=f)
                    num +=1
                    idlist.append(item.id)
                if num == 10000:
                    print(word + ' done 1000 times, next word. {0} words finished'.format(wordnum))
                    break
            print(word + ' done, next word. {0} words finished'.format(wordnum))
    if word == 'vile':
        contin = 1