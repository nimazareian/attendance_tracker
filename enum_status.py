import enum

# status of when student scans card
class Status(enum.Enum):
    LOGGED_IN = 1
    LOGGED_OUT = 2
    ALREADY_LOGGED_OUT = 3
    NOT_FOUND = 4
