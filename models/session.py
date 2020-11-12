"""
-----------------------------
  The Point Is to Change It - Sessions Model
-----------------------------

Contained in Sessions.py:
1. class definition for Session entities

"""

from models import Base


class Session(Base):
    """
    Session class stores sessions and their associated user ids
    """
    def __init__(self, *args, **kwargs):
        """ init """
        from datetime import datetime
        self.start = datetime.now()
        self.ttl = 10
        super().__init__(*args, **kwargs)
    
    def expired(self):
        """ check if session has expired """
        from datetime import timedelta
        if self.start > self.start + timedelta(seconds=self.ttl):
            return True
        return False