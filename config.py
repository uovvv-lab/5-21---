import os

BASE_DIR = os.path.dirname(__file__) #현재 폴더경로 가져오는 명령

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY="dev"