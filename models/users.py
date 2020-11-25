from models.base import Base

class User(Base):
    """ User class """
    def __init__(self, *args, **kwargs):
        """ init """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.handle = kwargs.get('handle')
        self.password = kwargs.get('password')
        self.collectives = []
        self.roles = []
        self.invitations_into_collectives = []
        self.my_requests_to_join_collectives = []
        self.notifications = []
        self.save_to_db()