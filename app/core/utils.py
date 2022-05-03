import ulid


def get_ulid() -> str:
    return ulid.new().str
