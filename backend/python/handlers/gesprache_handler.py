import json
from sprachweg.gesprach_kontroller import gesprach_erstellen, gesprach_laden, gesprach_speichern, gesprach_compiler, alle_gesprache_erhalten


def alle_gesprache_erhalten_handler():

    try:
        dateien_namen = alle_gesprache_erhalten()

        return json.dumps({'dateien_namen': dateien_namen}), 200
    except Exception as e:
        return json.dumps({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500
    

def gesprach_laden_handler(content : dict):

    anfragedaten = content

    if not anfragedaten:
        return json.dumps({"antwort": "Keine JSON-Daten erhalten"}), 400

    print(anfragedaten)

    gesprach_name = anfragedaten.get("gesprach_name")

    if not gesprach_name:
        return json.dumps({"antwort": "Es braucht einen Name bitte"}), 400

    try:
        gesprach = gesprach_laden(gesprach_name)
        kompilierte_gesprach = gesprach_compiler(gesprach)

        return json.dumps({'nachricht': 'Das Gespräch wurde geladen', "gesprach": kompilierte_gesprach}), 200
    except Exception as e:
        return json.dumps({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500
    

def gesprach_erstellen_handler(content : dict):
    anfragedaten = content

    if not anfragedaten:
        return json.dumps({"antwort": "Keine JSON-Daten erhalten"}), 400

    # print(anfragedaten)
    # print("-------------------------------------------------------------------------")

    gesprach_name = anfragedaten.get("gesprach_name")
    personlichkeit = anfragedaten.get("personlichkeit", None)

    if not gesprach_name:
        return json.dumps({"antwort": "Es braucht einen Name bitte"}), 400

    try:
        gesprach = gesprach_erstellen(gesprach_name, personlichkeit)

        kompilierte_gesprach = gesprach_compiler(gesprach)

        return json.dumps({'nachricht': 'Das Gespräch wurde erstellt', "gesprach": kompilierte_gesprach}), 200
    except Exception as e:
        return json.dumps({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500