from typing import TypedDict


class AtprotoInfo(TypedDict):
    handle: str
    password: str


class AtprotoUser(TypedDict):
    did: str
    display_name: str | None
    handle: str
