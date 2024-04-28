from atproto import Client

from dotenv import load_dotenv
from type_dicts.atproto import AtProtoInfo
from utils import AtProtoUtils, EnvironmentUtils

load_dotenv()

client = Client(
    base_url='https://bsky.social'
)


atproto_info: AtProtoInfo = {
    "handle": EnvironmentUtils.get_env_variable(
        "ATPROTO_HANDLE"
    ),
    "password": EnvironmentUtils.get_env_variable(
        "ATPROTO_PASSWORD"
    )
}

atproto_utils = AtProtoUtils(
    client,
    atproto_info
)
