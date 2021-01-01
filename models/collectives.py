from models.base import Base

class Collective(Base):
    """ User class """
    def __init__(self, *args, **kwargs):
        """ init """
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name')
        self.handle = kwargs.get('handle')
        self.email = kwargs.get('email')
        self.profile_picture = kwargs.get('profile_picture')
        self.will = kwargs.get('will')
        self.authorities_granted = kwargs.get('authorities_granted')
        self.authorities_recieved = kwargs.get('authorities_recieved')
        self.members = []
        self.internal_props = []
        self.external_props = []
        self.internal_posts = []
        self.public_posts = []
        self.internal_tasks = []
        self.external_tasks = []
        self.internal_dues_amount = ''
        self.internal_dues_frequency = ''
        self.collectives = []
        self.roles_occupied = []
        self.roles_contained = []
        self.invitations_into_collectives = []
        self.my_requests_to_join_collectives = []
        self.requests_to_join_this_collective = []
        self.notifications = []
        self.save_to_db()