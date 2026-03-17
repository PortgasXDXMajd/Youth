from contextvars import ContextVar

_current_actor: ContextVar[str] = ContextVar("current_actor", default="system")


def set_current_actor(actor: str) -> None:
    _current_actor.set(actor or "system")


def get_current_actor() -> str:
    return _current_actor.get()


def clear_current_actor() -> None:
    _current_actor.set("system")
