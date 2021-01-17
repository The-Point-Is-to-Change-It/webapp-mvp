"""
helper functions
"""

def build_url(endpoint):
    # in deployment
    # return 'https://the-point-is-to-change-it-v0.uc.r.appspot.com/' + endpoint
    # in development
    return 'http://127.0.0.1:8080/' + endpoint
