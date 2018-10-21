import praw
import time
from _file import File
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.ini')

client_secret = config['reddit']['client_secret']
client_id = config['reddit']['client_id']
username = config['reddit']['username']
password = config['reddit']['password']
user_agent = config['reddit']['user_agent']

api = praw.Reddit(client_id=client_id,
                  client_secret=client_secret,
                  user_agent=user_agent,
                  username=username,
                  password=password)

threads = File('threads.txt')
submissions = []
for s in api.redditor('izdwuut').submissions.new():
    if s.subreddit == 'GiftofGames':
        if '[Offer]'.lower() in s.title.lower():
            if s.over_18 and not threads.contains(s.fullname):
                print('Processing: ' + s.title)
                submissions.append(s)
                for c in s.comments:
                    c.upvote()
                    print(c.fullname + ' upvoted!')
                    time.sleep(2)
                threads.add_line(s.fullname)
                time.sleep(2)
threads.close()