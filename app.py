from flask import Flask, render_template, request, jsonify

from models import *

app = Flask(__name__)

# Déclaration de l'objet Competition
# contenant une liste d'arènes
arenes = [None] + [Arene(x+1, Combattant(f"Rouge{x+1}"), Combattant(f"Vert{x+1}"), Chronometre(3*60)) for x in range(5)]
competition = Competition(arenes)

@app.route('/affichage/<int:id_arene>')
def affichage(id_arene):
    if 0 < id_arene < len(competition.arenes):
        return render_template('affichage.html', 
            arene=competition.arenes[id_arene])
    else:
        return "Il n'y a pas d'arène avec ce numéro"

@app.route('/bandeau/<int:id_arene>')
def bandeau(id_arene):
    if 0 < id_arene < len(competition.arenes):
        return render_template('bandeau.html', 
            arene=competition.arenes[id_arene])
    else:
        return "Il n'y a pas d'arène avec ce numéro"

@app.route('/Arene/<int:id_arene>')
def arene(id_arene):
    if 0 < id_arene < len(competition.arenes):
        return render_template('arbitrage.html', 
            arene=competition.arenes[id_arene])
    else:
        return "Il n'y a pas d'arène avec ce numéro"


################### Routes pour la configuration ###################
@app.route('/configuration')
def configuration():
    return render_template('config.html',
        competition=competition)


@app.route('/changer-nom/<int:id_arene>', methods=['POST'])
def changeNomCbt(id_arene):
    data = request.json
    nom_cbt_rouge = data.get('nom_cbt_rouge')
    nom_cbt_vert = data.get('nom_cbt_vert')
    competition.arenes[id_arene].combattants['rouge'].nom = nom_cbt_rouge
    competition.arenes[id_arene].combattants['vert'].nom = nom_cbt_vert
    return jsonify(arene=competition.arenes[id_arene].to_json())

@app.route('/ajouter-arene', methods=['POST'])
def ajouterArene():
    x = len(competition.arenes)
    a = Arene(x, Combattant(f"Rouge{x}"), Combattant(f"Vert{x}"), Chronometre(3*60))
    competition.ajouterArene(a)
    return jsonify(arene=a.to_json())

@app.route('/supprimer-arene', methods=['POST'])
def supprimerArene():
    # pour le moment, supprime la dernière arène
    _id = competition.supprimerArene(-1)._id
    return {'message': f'Arène {_id} supprimée'}

@app.route('/reset/<int:id_arene>', methods=['POST'])
def resetArene(id_arene):
    competition.arenes[id_arene].reset()
    return jsonify(arene=competition.arenes[id_arene].to_json())


################### Routes pour le timer ###################
@app.route('/start-timer/<int:id_arene>', methods=['POST'])
def startTimer(id_arene):
    competition.arenes[id_arene].chrono.start()
    return {"message": f"arene {id_arene} started"}

@app.route('/pause-timer/<int:id_arene>', methods=['POST'])
def pauseTimer(id_arene):
    competition.arenes[id_arene].chrono.pause()
    return {"message": f"arene {id_arene} paused"}

@app.route('/reset-timer/<int:id_arene>', methods=['POST'])
def resetTimer(id_arene):
    competition.arenes[id_arene].chrono.reset()
    return {"message": f"arene {id_arene} reset"}

@app.route('/add-seconds/<int:id_arene>/<int:seconds>', methods=['POST'])
def addSeconds(id_arene, seconds):
    competition.arenes[id_arene].chrono.addSeconds(seconds)
    return {"message": f"added {seconds}s to arene {id_arene}"}

@app.route('/sub-seconds/<int:id_arene>/<int:seconds>', methods=['POST'])
def subSeconds(id_arene, seconds):
    competition.arenes[id_arene].chrono.subSeconds(seconds)
    return {"message": f"remove {seconds}s to arene {id_arene}"}

################### Routes pour l'arbitrage ###################
@app.route('/increment-score/<int:id_arene>/<combattant>/<int:valeur>', methods=['POST'])
def incrementScore(id_arene, combattant, valeur):
    competition.arenes[id_arene].incrementerScore(combattant, valeur)
    return jsonify(arene=competition.arenes[id_arene].to_json()) 

@app.route('/increment-carton/<int:id_arene>/<combattant>/<couleur>', methods=['POST'])
def incrementCarton(id_arene, combattant, couleur):
    competition.arenes[id_arene].ajouterCarton(combattant, couleur)
    return jsonify(arene=competition.arenes[id_arene].to_json())

@app.route('/annuler/<int:id_arene>', methods=['POST'])
def annulerAction(id_arene):
    if len(competition.arenes[id_arene].historique) != 0:
        competition.arenes[id_arene].annulerDerniereAction()
    return jsonify(arene=competition.arenes[id_arene].to_json())

################### Routes pour l'affichage ###################
@app.route('/infos/<int:id_arene>', methods=['POST'])
def infos(id_arene):
    return jsonify(arene=competition.arenes[id_arene].to_json())

if __name__ == '__main__':
    # L'application écoute sur toutes les interfaces réseau (0.0.0.0) sur le port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
