from utils.atproto import AtprotoUtils
from utils.database import DatabaseUtils
from _messages import messages
import random
import schedule
import time
from _type_dicts import AtprotoUser


class PostNewFollowers:
    running = False

    def __init__(self, atproto_utils: AtprotoUtils) -> None:
        self.atproto_utils = atproto_utils

    def post_new_followers(self):
        client = self.atproto_utils.client
        if client.me is None:
            raise Exception("Failed to login.")
        bot_did = client.me.did
        followers = client.get_followers(bot_did).followers
        database = DatabaseUtils()

        for follower in followers:
            follower_info: AtprotoUser = {
                "did": follower.did,
                "display_name": follower.display_name,
                "handle": follower.handle
            }
            atproto_user = database.find_user(follower.did)
            if atproto_user is None:
                if database.insert_user(follower_info) == True:
                    # message = random.choice(messages)
                    # message.replace("<USER_HANDLE>", follower.handle)
                    message = "test"
                    self.atproto_utils.post(message)

    def start_cron(self):
        # self.post_new_followers()
        schedule.every(5).minutes.do(self.post_new_followers)
        running = True

        while running:
            schedule.run_pending()
            time.sleep(1)
