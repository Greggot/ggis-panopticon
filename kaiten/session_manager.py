import json
from kaiten.session import Session
from kaiten.user import User

def get_session(path = 'env/env.json') -> tuple[User, Session]:
    env = ""
    
    with open(path) as env_file: 
        env = json.loads(env_file.read())

    session = Session(server=env['kaiten_host'], token=env['kaiten_token'])
    user = User(session)
    return (user, session)