import smtplib, ssl
import json
import requests


def load_json(path):
    return json.load(open(path))

def check_backwater(request_url):
    reply = requests.get(request_url)
    if "Animal is No Longer Available" in reply.text: result = False
    elif "Animal is No Longer in Stock" in reply.text: result = False
    else: result = True

    d = json.loads(reply.text.split("(")[1].split(")")[0])['product']

    return {'in_stock':result, 'name':d['name'], 'site':'backwater reptiles: https://backwaterreptiles.com'}

def send_email(recipient, message):
    keys = load_json("../credentials.json")

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = keys['gmail']['addr']  # Enter your address
    password = keys['gmail']['pass']

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        result = server.sendmail(sender_email, recipient, message)
    
    return result

if __name__ == "__main__":
    tocheck = load_json("../tocheck.json")

    backwater = tocheck['backwater']
    in_stock = []

    for link in backwater:
        result = check_backwater(link)
        if result['in_stock'] == True:
            in_stock.append(result)
    
    if in_stock:
        print("Found some!")
        print("Sending message:")
        message = """\
Subject: You have {} frogs in stock.

{}

This message is sent from Python.""".format(len(in_stock), str(in_stock))
        print(message)

        send_email(load_json("../credentials.json")['recipient'], message)
