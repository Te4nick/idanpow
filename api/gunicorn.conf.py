from os import environ


bind = "127.0.0.0:8000"
wsgi_app = "idanpow.wsgi:application"
workers = 4
threads = 2
