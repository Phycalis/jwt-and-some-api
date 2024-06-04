from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


print(Role.USER.value)
