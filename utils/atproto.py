from atproto import Client
from type_dicts.atproto import AtProtoInfo


class AtProtoUtils:
    def __init__(self, client: Client, atproto_info: AtProtoInfo) -> None:
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

    def post(self, content):
        self.client.send_post(content)
