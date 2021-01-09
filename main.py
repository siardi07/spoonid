import os, sys, traceback, json

try:
    import requests
except:
    os.system("pip install --upgrade pip")
    os.system("pip install requests")
    import requests

try:
    from websocket import create_connection
except:
    os.system("pip install websocket-client")
    from websocket import create_connection

try:
    from fake_useragent import UserAgent
except:
    os.system("pip install fake-useragent")
    from fake_useragent import UserAgent

jsondb = "db.johnson"

def login(nomor, password):
    try:
        ua = UserAgent()
        uafix = ua.random
        headers = {
            "User-Agent": uafix,
            "origin": "https://www.spooncast.net",
            "referer": "https://www.spooncast.net/",
            "content-type": "application/json"
        }
        jsons = {
            "device_unique_id": uafix,
            "auth_data": {
                "act_type": "phone",
                "password": password,
                "msisdn": nomor
            }
        }
        tokens = requests.post("https://id-auth.spooncast.net/tokens", headers=headers, json=jsons).json()
        jwt = tokens["data"]["jwt"]
        rtokenvalue = tokens["data"]["refresh_token"]

        #update headers dengan pair key baru
        headers["Authorization"] = "Bearer "+jwt

        jsonlogin = {
            "sns_type" : "phone",
            "sns_id" : nomor,
            "password" : password
        }
        login = requests.post("https://id-api.spooncast.net/signin/?version=2", headers=headers, json=jsonlogin).json()
        print(login)
        uid = str(login["results"][0]["id"])
        uname = login["results"][0]["nickname"]
        utag = login["results"][0]["tag"]
        config = {}

        config["nomor"] = nomor
        config["password"] = password
        config["uid"] = uid
        config["uname"] = utag
        config["utag"] = uname
        config["uafix"] = uafix
        config["jwt"] = jwt
        config["rtokenvalue"] = rtokenvalue

        with open(jsondb, "w") as jsonFile:
            json.dump(config, jsonFile, indent=2)

        print("berhasil login")
        return 1

    except:
        print(traceback.format_exc())
        print(tokens)
        print("id/anjim password salah bego")
        return 0

def gantiid(config):
    try:
        headers = {
            "Authorization": "Bearer " + config["jwt"],
            "User-Agent": config["uafix"],
            "origin": "https://www.spooncast.net",
            "referer": "https://www.spooncast.net/",
            "accept": "application/json",
            "host": "id-api.spooncast.net",
        }
        newid = input("Masukkan id baru : @")
        json = {
            "username": newid
        }

        changeid = requests.post("https://id-api.spooncast.net/users/username/", headers=headers, json=json).json()
        print(changeid)
    except:
        print(traceback.format_exc())



if __name__ == '__main__':
    #input

    print("Hai kalian salam kenal dari aku Awvirgo\ncontoh : 6212345678910")
    nomor = input("Masukkan nomor telepon yang terhubung pada akun : ")
    password = input("Masukkan password : ")

    #selection
    if nomor[:1] == '0':
        nomor = '62'+nomor[1:]


    ref = login(nomor, password)
    #login handler
    if ref == 0:
        print("id/anjim password salah bego . silahkan ganti akun")
        os.execv(sys.executable, ['python'] + sys.argv)

    with open(jsondb, "r") as jsonFile:
        config = json.load(jsonFile)

    gantiid(config)

    print("Enjoy ~")


