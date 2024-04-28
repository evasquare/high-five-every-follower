from atproto import Client

from dotenv import load_dotenv
from _type_dicts import AtprotoInfo
from utils import AtprotoUtils, EnvironmentUtils
from events import PostNewFollowers

load_dotenv()

client = Client(
    base_url=EnvironmentUtils.get_env_variable(
        "ATPROTO_BASE_URL"
    )
)

atproto_info: AtprotoInfo = {
    "handle": EnvironmentUtils.get_env_variable(
        "ATPROTO_HANDLE"
    ),
    "password": EnvironmentUtils.get_env_variable(
        "ATPROTO_PASSWORD"
    )
}

atproto_utils = AtprotoUtils(
    client,
    atproto_info
)

post_new_followers = PostNewFollowers(atproto_utils).start_cron()
