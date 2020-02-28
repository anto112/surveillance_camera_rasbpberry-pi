import requests
import datetime

# reference here "https://notify-bot.line.me/en/"

def timestamp():
    tstring = datetime.datetime.now()
    print("Filename generated ...")
    return tstring.strftime("%Y-%m-%d_%H:%M:%S")

def send_notif(name_file):
    local_file = timestamp()
    url = "https://notify-api.line.me/api/notify"
    access_token = '3Yyp70il4KWpv5mcJuj1sfPOtsd9vNId9ENGN7IMvPN'
    headers = {'Authorization': 'Bearer ' + access_token}
    message = 'some object detected\n' + local_file
    image = name_file
    payload = {'message': message}
    files = {'imageFile': open(image, 'rb')}
    r = requests.post(url, headers=headers, params=payload, files=files,)