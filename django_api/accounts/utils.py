import requests


def send_hook(username, ip_addr):
    header = {"Content-type": "application/json"}
    payload = {
        "user": username,
        "ip": ip_addr,
    }

    r = requests.post(
        "https://encrusxqoan0b.x.pipedream.net/", json=payload,
    )
