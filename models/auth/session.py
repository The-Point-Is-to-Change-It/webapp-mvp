"""
-----------------------------
  The Point Is to Change It | Models - Session
-----------------------------

Models - Session Contains:
1. Session class for creating, checking, and destroying sessions
2. Everything related to user authentication

"""
from models.base import Base


class Session(Base):
    """ Session class """
    exp_time = 3333
    sessions = {}

    def __init__(self, *args, **kwargs):
        """ init """
        from datetime import datetime
        super().__init__(*args, **kwargs)
        self.created_at = datetime.utcnow()
        self.user_id = kwargs.get('user_id')
        Session.sessions[self.id] = {
            'user_id': self.user_id,
            'created_at': self.created_at
        }
        self.save_to_db()

    @classmethod
    def expired(cls, dict_repr):
        """
        check if session has expired. True if it has, False otherwise.
        """
        from datetime import datetime, timedelta
        import pytz
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if now > (dict_repr['created_at'] + timedelta(seconds=Session.exp_time)):
            cls.delete_from_db_with_dict(dict_repr)
            return True
        return False
    