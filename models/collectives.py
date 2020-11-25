from models.base import Base

class Collective(Base):
    """ User class """
    def __init__(self, *args, **kwargs):
        """ init """
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username')
        self.handle = kwargs.get('handle')
        self.members = []
        self.internal_proposals = []
        self.internal_posts = []
        self.public_posts = []
        self.internal_tasks = []
        self.internal_dues = ''
        self.collectives = []
        self.roles = []
        self.invitations_into_collectives = []
        self.my_requests_to_join_collectives = []
        self.requests_to_join_this_collective = []
        self.notifications = []
        self.save_to_db()