import ulid
from pydantic import EmailStr



def get_ulid():
    return ulid.new().str



