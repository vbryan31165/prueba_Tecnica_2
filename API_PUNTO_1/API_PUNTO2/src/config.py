from distutils.command import config
from distutils.debug import DEBUG


class Developmentconfig():
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD=''
    MYSQL_DB='api_noticias'

config={
    'development': Developmentconfig
}