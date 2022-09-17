from enum import Enum
from pickle import NONE 

CS_WINS = ["A", "B", "C", "D", "E"]
CS_LOSSES = ["a", "b", "c", 'd', "e"]

NULL = 0

# events:
class events(Enum):
    BEGIN = 0
    CONSECUTIVE_WIN = 1
    CONSECUTIVE_LOSS = 2
    STEP_WIN = 3
    STEP_LOSS = 4

# step updates:
WIN = 1
LOSS = 2

# reset constants
class reset_(Enum):
    RESET_CSWIN = 0
    RESET_CSLOSS = 1
    RESET_STEPWIN = 2
    RESET_STEPLOSS = 3

class service(Enum):
    # service
    NONE = -1
    USER_SERVE = 0
    OPPONENT_SERVE = 1


# set complete
COMPLETE = 1
NOT_COMPLETE = 2