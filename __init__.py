from _type_dicts import AtprotoInfo
from atproto import Client
from dotenv import load_dotenv
from events import PostNewFollowers
from utils import AtprotoUtils, EnvironmentUtils, ThreadManager


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

thread_queue = [
    PostNewFollowers(
        atproto_utils
    ).start_cron
]

# This blocks the main thread.
ThreadManager(thread_queue).start_tasks()
