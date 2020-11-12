from blueprints.dashboard import dash

@dash.route('/', methods=['GET'], strict_slashes=False)
def index():
    return 'this is dashboard'