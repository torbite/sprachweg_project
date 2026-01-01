import flask, flask_cors
from flask import Flask, jsonify, request
import gesprach_kontroller, ki_kontroller
from gesprach_kontroller import gesprach_erstellen, gesprach_laden, gesprach_speichern, gesprach_compiler, alle_gesprache_erhalten
from ki_kontroller import nachricht_an_gesprach_senden

app = Flask(__name__)
app.config['DEBUG'] = True
flask_cors.CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/alle_gesprache_erhalten', methods=['GET'])
def alle_gesprache_erhalten_handler():

    try:
        dateien_namen = alle_gesprache_erhalten()

        return jsonify({'dateien_namen': dateien_namen}), 200
    except Exception as e:
        return jsonify({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500


@app.route('/nachricht_senden', methods=['POST'])
def nachricht_senden_handler():

    anfragedaten = request.get_json()

    if not anfragedaten:
        return jsonify({"antwort": "Keine JSON-Daten erhalten"}), 400

    print(anfragedaten)

    gesprach_name = anfragedaten.get("gesprach_name")
    nachricht = anfragedaten.get("nachricht")

    if not gesprach_name or not nachricht:
        return jsonify({"antwort": "eingebt ein korrekt Gespräch name und eingebt eine nachricht bitte"}), 400

    try:
        gesprach = gesprach_laden(gesprach_name)
        gesprach_inhalt = nachricht_an_gesprach_senden(nachricht, gesprach)

        kompilierte_gesprach = gesprach_speichern(gesprach_name, gesprach_inhalt)

        return jsonify({'antwort': 'Die nachricht wurde richtig gesendet', "gesprach" : kompilierte_gesprach}), 200
    except Exception as e:
        print(e)
        return jsonify({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500

@app.route('/gesprach_laden', methods=['POST'])
def gesprach_laden_handler():

    anfragedaten = request.get_json()

    if not anfragedaten:
        return jsonify({"antwort": "Keine JSON-Daten erhalten"}), 400

    print(anfragedaten)

    gesprach_name = anfragedaten.get("gesprach_name")

    if not gesprach_name:
        return jsonify({"antwort": "Es braucht einen Name bitte"}), 400

    try:
        gesprach = gesprach_laden(gesprach_name)
        kompilierte_gesprach = gesprach_compiler(gesprach)

        return jsonify({'nachricht': 'Das Gespräch wurde geladen', "gesprach": kompilierte_gesprach}), 200
    except Exception as e:
        return jsonify({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500

@app.route('/gesprach_erstellen', methods=['POST'])
def gesprach_erstellen_handler():
    anfragedaten = request.get_json()

    if not anfragedaten:
        return jsonify({"antwort": "Keine JSON-Daten erhalten"}), 400

    # print(anfragedaten)
    # print("-------------------------------------------------------------------------")

    gesprach_name = anfragedaten.get("gesprach_name")
    personlichkeit = anfragedaten.get("personlichkeit", None)

    if not gesprach_name:
        return jsonify({"antwort": "Es braucht einen Name bitte"}), 400

    try:
        gesprach = gesprach_erstellen(gesprach_name, personlichkeit)

        kompilierte_gesprach = gesprach_compiler(gesprach)

        return jsonify({'nachricht': 'Das Gespräch wurde erstellt', "gesprach": kompilierte_gesprach}), 200
    except Exception as e:
        return jsonify({"antwort" : "Einen Fehler hat passiert", "fehler_nachricht" : e}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)
