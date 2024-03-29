import json
with open("jsonformatter.txt", mode='r') as file:
    __configs = json.load(file)

def get_host() -> str:
    return __configs['host']

def get_name() -> str:
    return __configs['user']

def get_password() -> str:
    return __configs['password']

def db_url() -> str:
    return __configs['db_name']
