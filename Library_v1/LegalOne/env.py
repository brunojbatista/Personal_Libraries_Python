import os

ENV = {
    "office": "rpa2",
    "login": "regispontesti",
    "password": "U93#a%O5DOLq",
}

for key in ENV: os.environ[key] = ENV[key]

def get_env(env_key: str):
    return os.environ[env_key]
