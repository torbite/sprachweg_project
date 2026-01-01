import requests, json

BASE_URL = "http://localhost:4000/"
NACHRICHT_SENDEN_URL = "http://localhost:4000/nachricht_senden"
GESPRACH_LADEN_URL = "http://localhost:4000/gesprach_laden"
GESPRACH_ERSTELLEN_URL = "http://localhost:4000/gesprach_erstellen"

antwort = requests.post(GESPRACH_ERSTELLEN_URL, json=json.dumps({"gesprach_name" : "elizabeth"}))
print(antwort.content)
print()
print()
print(json.loads(antwort.content))
input("1----")
print()
antwort = requests.post(GESPRACH_LADEN_URL, json=json.dumps({"gesprach_name" : "elizabeth"}))
print(json.loads(antwort.content))
input("2----")
print()
antwort = requests.post(NACHRICHT_SENDEN_URL, json=json.dumps({"gesprach_name" : "elizabeth", "nachricht" : "hallo!"}))
print(json.loads(antwort.content))
input("3----")

