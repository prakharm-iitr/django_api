import logging
import requests

logging.basicConfig(filename='app.log', filemode='w')


# Function to send webhhook
def send_hook(username, ip_addr):
    payload = {
        "user": username,
        "ip": ip_addr,
    }

    # Ideally should use Python Retry to make multiple requests if one fails
    # One request may fail due to server congestion
    # TODO: Implement n retries
    try:
        r = requests.post(
            "https://encrusxqoan0b.x.pipedream.net/", json=payload, timeout=5
        )
    except requests.Timeout as err:
        logging.error({"message": err.message})
    except Exception as err:
        logging.error({"message": err.message})
