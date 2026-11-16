from enum import Enum

class RefreshTokenStatusEnum(Enum):
    ACTIVE = "active"
    ROTATED = "rotated"
    REVOKED = "revoked"
