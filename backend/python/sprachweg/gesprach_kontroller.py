import json, os, hashlib, boto3, uuid
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage, FunctionMessage
from pathlib import Path

# kontext = "Du musst ein Gespräch auf Deutsch führen. Du können nicht unter allen Umständen andere Sprachen sprachen. Aber du musst es wissen, das der Benutzer ist ein Anfänger."
BASEKONTEXT = "Du musst ein Gespräch auf Deutsch führen. Du können nicht unter allen Umständen andere Sprachen sprachen.\nDu bist ein Personn, auf Deutschland, also verhalten dich normal"
BASEPFAD = os.getenv("BASEPFAD")
GESPRACHEN_DATEIPFAD = f"{BASEPFAD}/backend/gesprachen"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('alle_gesprache')

typ_worterbuch = {
    SystemMessage("").type : SystemMessage,
    AIMessage("").type : AIMessage,
    HumanMessage("").type : HumanMessage
}

def alle_gesprache_erhalten():
    global GESPRACHEN_DATEIPFAD

    ordner = Path(GESPRACHEN_DATEIPFAD)

    dateien = [p.name for p in ordner.iterdir() if p.is_file()]

    return dateien

def gesprach_compiler(gesprach_liste):
    kompiliert_liste = []

    for langchain_nachricht in gesprach_liste:
        try:
            nachrichteninhalt = langchain_nachricht.content
            nachrichtentyp = langchain_nachricht.type

            nachricht = {
                "typ" : nachrichtentyp,
                "inhalt" : nachrichteninhalt
            }

            kompiliert_liste.append(nachricht)
        except:
            print(f"Das Nachrict ist ein lanchain_nachricht nicht: {langchain_nachricht}")
            continue
    return kompiliert_liste

def gesprach_dekompilieren(kompiliert_liste):
    global typ_worterbuch
    gesprach_liste = []

    for kompiliert_nachricht in kompiliert_liste:
        try:
            nachrichteninhalt = kompiliert_nachricht["inhalt"]
            nachrichtentyp = kompiliert_nachricht["typ"]

            gesprach_liste.append(typ_worterbuch[nachrichtentyp](nachrichteninhalt))
        except:
            print(f"Etwas ist falsch mit dem Nachricht")
            continue
    return gesprach_liste

def gesprach_laden(gesprach_name):
    global GESPRACHEN_DATEIPFAD

    dateiname = f"{GESPRACHEN_DATEIPFAD}/{gesprach_name}.json"

    print(f"""
Gespräch name = {gesprach_name}
dateiname     = {dateiname}
""")
    try:
        with open(dateiname, "r") as datei:
            dateiinhalt = json.load(datei)
        

        print(f"dateiinhalt        = {dateiinhalt}")

        antwort = gesprach_dekompilieren(dateiinhalt)

        return antwort
    except Exception as e:
        print(f"Exception: {e}")
        return None

def gesprach_speichern(gesprach_name, gesprach_inhalt):
    dateiname = f"{GESPRACHEN_DATEIPFAD}/{gesprach_name}.json"

    kompilierte_gesprach = gesprach_compiler(gesprach_inhalt)

    with open(dateiname, "w") as datei:
        json.dump(kompilierte_gesprach, datei, indent=4)

    return kompilierte_gesprach


def gesprach_erstellen(gesprach_name, personlichkeit = None):
    global BASEKONTEXT, GESPRACHEN_DATEIPFAD

    # dateiname = f"{GESPRACHEN_DATEIPFAD}/{gesprach_name}.json"

    if personlichkeit:
        gesprach_kontext = f"{BASEKONTEXT}.\nPersonlity: {personlichkeit}"
    else:
        gesprach_kontext = BASEKONTEXT


    gesprach_nachrichten = [
       SystemMessage(gesprach_kontext)
    ]

    kompiliert_nachrichten = gesprach_compiler(gesprach_nachrichten)

    id = uuid.uuid4().hex

    gesprach_artikel = {

    }

    with open(dateiname, "w") as datei:
        json.dump(kompiliert_nachrichten, datei, indent=4)

    return gesprach_nachrichten
    


def gesprach_zeigen(gesprach):
    for nachricht in gesprach:
        inhalt = nachricht.content
        typ = nachricht.type

        print(f"{typ}: \n---- {inhalt}")
        print()