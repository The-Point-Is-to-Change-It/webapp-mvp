from models.base import Base

class ProfileInformation(Base):
    """ public information about a given entity """
    def __init__(self, *args, **kwargs):
        """ init """
        super().__init__(*args, **kwargs)
        self.community_interests = []
        self.values = []
        self.project_interests = []
        self.big_why = ''



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
        profileInfo = ProfileInformation()
        self.profile_info = profileInfo.id
        self.save_to_db()

    
