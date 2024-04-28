from atproto import Client
from dotenv import load_dotenv
from _type_dicts import AtprotoInfo
from utils import AtprotoUtils, EnvironmentUtils
from events import PostNewFollowers
import threading
import time

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

thread = threading.Thread(target=PostNewFollowers(
    atproto_utils).start_cron, daemon=True)
thread.start()

try:
    print("Bot is Running...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("")
