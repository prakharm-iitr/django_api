import requests


# Function to send webhhook
def send_hook(username, ip_addr):
    payload = {
        "user": username,
        "ip": ip_addr,
    }

    r = requests.post(
        "https://encrusxqoan0b.x.pipedream.net/", json=payload,
    )
