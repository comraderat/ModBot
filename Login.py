import requests

def Login(session, username, password):
    url = "https://sys.8ch.net/mod.php?/"
    data = {"username": username,
            "password": password,
            "login": "Continue:"
            }
    r = session.post(url, data)