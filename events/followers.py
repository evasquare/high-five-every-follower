from utils.atproto import AtprotoUtils
from utils.database import DatabaseUtils
from _messages import messages
import random
import schedule
import time
from _type_dicts import AtprotoUser
from atproto import client_utils
from atproto_client.models.app.bsky.actor.defs import ProfileView


class PostNewFollowers:
    running = False

    def __init__(self, atproto_utils: AtprotoUtils) -> None:
        self.atproto_utils = atproto_utils

    def track_followers(self):
        client = self.atproto_utils.client
        if client.me is None:
            raise Exception("Failed to login.")

        bot_did = client.me.did
        followers = client.get_followers(bot_did).followers

        for follower in followers:
            self.dostuff(follower)

    def dostuff(self, follower: ProfileView):
        database = DatabaseUtils()
        follower_info: AtprotoUser = {
            "did": follower.did,
            "display_name": follower.display_name,
            "handle": follower.handle,
            "post_cid": None
        }
        atproto_user = database.find_follower(follower.did)

        if atproto_user is None and database.insert_follower(follower_info):
            message = random.choice(messages)
            created_post = None

            if message.find("<USER_HANDLE>") and message.count("<USER_HANDLE>") == 1:
                split = message.split("<USER_HANDLE>")
                sending_text = client_utils.TextBuilder()
                sending_text.text(split[0])
                sending_text.mention(
                    text="@" + follower.handle, did=follower.did)
                for item in split[1:]:
                    sending_text.text(item)
                created_post = self.atproto_utils.post(sending_text)
            else:
                sending_text = message.replace(
                    "<USER_HANDLE>", "@" + follower.handle)
                created_post = self.atproto_utils.post(sending_text)

            if created_post:
                follower_info["post_cid"] = created_post
                database.update_follower(follower_info)

    def start_cron(self):
        self.track_followers()
        schedule.every(1).minutes.do(self.track_followers)
        running = True

        while running:
            schedule.run_pending()
            time.sleep(1)
