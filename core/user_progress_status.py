from enum import Enum

# Define an enumeration class
class UserProgressStatus(Enum):
    LOCKED = "LOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"