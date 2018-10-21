import praw
import time
from configparser import ConfigParser
from tqdm import tqdm
import os

from _file import File


class Upvoter:
    def _get_api(self):
        config = self.config['reddit']
        client_secret = config['client_secret']
        client_id = config['client_id']
        username = config['username']
        password = config['password']
        user_agent = config['user_agent']

        api = praw.Reddit(client_id=client_id,
                          client_secret=client_secret,
                          user_agent=user_agent,
                          username=username,
                          password=password)

        return api

    def upvote(self):
        threads = File(self.config['general']['threads'])
        username = self.config['reddit']['username']
        for s in self.api.redditor(username).submissions.new():
            if s.subreddit == 'GiftofGames':
                if '[Offer]'.lower() in s.title.lower():
                    if s.over_18 and not threads.contains(s.fullname):
                        print('Processing: ' + s.title)
                        for c in tqdm(s.comments):
                            if not c.author:
                                continue
                            c.upvote()
                            time.sleep(2)
                        threads.add_line(s.fullname)
                        time.sleep(2)
                        print()
        threads.close()

    def __init__(self, settings):
        self.config = ConfigParser(os.environ)
        self.config.read(settings)
        self.api = self._get_api()


if __name__ == '__main__':
    settings = 'settings.ini'
    upvoter = Upvoter(settings)
    upvoter.upvote()
