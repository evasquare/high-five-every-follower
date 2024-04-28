from _type_dicts import AtprotoInfo
from atproto import Client
from atproto_client.utils import TextBuilder


class AtprotoUtils:
    def __init__(self, client: Client, atproto_info: AtprotoInfo) -> None:
        self.client = client
        self.atproto_info = atproto_info
        self.login()

    def login(self):
        self.client.login(
            self.atproto_info['handle'],
            self.atproto_info["password"]
        )
        if self.client.me is None:
            raise Exception("Failed to login.")

    def post(self, text: str | TextBuilder):
        self.client.send_post(text)
