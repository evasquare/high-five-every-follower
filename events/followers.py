from utils.atproto import AtprotoUtils
from utils.database import DatabaseUtils
from _messages import messages
import random
import schedule
import time
from _type_dicts import AtprotoUser
from atproto import client_utils


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
            if atproto_user is None and database.insert_user(follower_info):
                message = random.choice(messages)

                if message.find("<USER_HANDLE>") and message.count("<USER_HANDLE>") == 1:
                    split = message.split("<USER_HANDLE>")
                    sending_text = client_utils.TextBuilder()
                    sending_text.text(split[0])
                    sending_text.mention(
                        text="@" + follower.handle, did=follower.did)
                    for item in split[1:]:
                        sending_text.text(item)
                    self.atproto_utils.post(sending_text)
                else:
                    sending_text = message.replace(
                        "<USER_HANDLE>", "@" + follower.handle)
                    self.atproto_utils.post(sending_text)

    def start_cron(self):
        self.post_new_followers()
        schedule.every(1).minutes.do(self.post_new_followers)
        running = True

        while running:
            schedule.run_pending()
            time.sleep(1)
