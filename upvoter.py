import os
from configparser import ConfigParser
from praw import Reddit

class Upvoter:
    def upvote(self):
        for comment in self.api.subreddit(self.config['reddit']['subreddit']).stream.comments():
            submission = comment.submission
            submission.upvote()
            comment.upvote()
            print('Processed comment {} in thread {}.'.format(comment.id, submission.url))

    def __init__(self, settings='settings.ini'):
        self.config = ConfigParser(os.environ)
        self.config.read(settings)
        self.api = Reddit(client_id=self.config['reddit']['client_id'],
                          client_secret=self.config['reddit']['client_secret'],
                          user_agent=self.config['reddit']['user_agent'],
                          username=self.config['reddit']['username'],
                          password=self.config['reddit']['password'])


if __name__ == '__main__':
    upvoter = Upvoter()
    upvoter.upvote()
