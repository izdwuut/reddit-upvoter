import os
from configparser import ConfigParser
from praw import Reddit
from tqdm import tqdm

class Upvoter:
    _api = None

    @property
    def api(self):
        if not self._api:
            config = self.config['reddit']
            client_secret = config['client_secret']
            client_id = config['client_id']
            username = config['username']
            password = config['password']
            user_agent = config['user_agent']

            self._api = Reddit(client_id=client_id,
                                    client_secret=client_secret,
                                    user_agent=user_agent,
                                    username=username,
                                    password=password)

        return self._api

    def upvote(self):
        for submission in self.api.subreddit(self.config['reddit']['subreddit']).stream.submissions():
            print('Processing thread {}.'.format(submission.title))
            submission.upvote()
            for comment in tqdm(submission.comments):
                comment.upvote()
            print()

    def __init__(self, settings='settings.ini'):
        self.config = ConfigParser(os.environ)
        self.config.read(settings)


if __name__ == '__main__':
    upvoter = Upvoter()
    upvoter.upvote()
