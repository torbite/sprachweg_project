from sprachweg.ki_kontroller import nachricht_an_gesprach_senden
from sprachweg.gesprach_kontroller import gesprach_laden, gesprach_speichern
import json

def nachricht_senden_handler(content : dict):

    anfragedaten = content

    if not anfragedaten:
        return json.dumps({"antwort": "Keine JSON-Daten erhalten"}), 400

    print(anfragedaten)

    gesprach_name = anfragedaten.get("gesprach_name")
    nachricht = anfragedaten.get("nachricht")

    if not gesprach_name or not nachricht:
        return json.dumps({"antwort": "eingebt ein korrekt Gespräch name und eingebt eine nachricht bitte"}), 400

    try:
        gesprach = gesprach_laden(gesprach_name)
        gesprach_inhalt = nachricht_an_gesprach_senden(nachricht, gesprach)

        kompilierte_gesprach = gesprach_speichern(gesprach_name, gesprach_inhalt)

        return json.dumps({'antwort': 'Die nachricht wurde richtig gesendet', "gesprach" : kompilierte_gesprach}), 200
    except Exception as e:
        print(e)
        return json.dumps({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500