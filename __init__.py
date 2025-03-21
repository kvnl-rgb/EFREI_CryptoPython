from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
import base64
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world(): #kaka
    return render_template('hello.html')

# Fonction pour vérifier et formater la clé
def validate_key(key):
    try:
        # Si la clé n'est pas une chaîne valide en base64 de 32 octets, 
        # on la transforme en une clé valide
        if len(key) < 32:
            # Padding de la clé si nécessaire
            key = key.ljust(32, '0')
        # Encodage en base64 (requis par Fernet)
        key_bytes = key[:32].encode()
        return base64.urlsafe_b64encode(key_bytes)
    except Exception:
        # En cas d'erreur, on retourne None
        return None

@app.route('/encrypt')
def encrypt_form():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cryptage</title>
    </head>
    <body>
        <h2>Cryptage avec clé personnalisée</h2>
        <form action="/encrypt/custom" method="post">
            <div>
                <label for="valeur">Texte à crypter :</label>
                <input type="text" id="valeur" name="valeur" required>
            </div>
            <div>
                <label for="cle">Votre clé personnelle (32 caractères max) :</label>
                <input type="text" id="cle" name="cle" required>
            </div>
            <button type="submit">Crypter</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/encrypt/custom', methods=['POST'])
def encrypt_custom():
    valeur = request.form.get('valeur', '')
    cle = request.form.get('cle', '')
    
    validated_key = validate_key(cle)
    if not validated_key:
        return "Erreur: Impossible de générer une clé valide à partir de votre entrée."
    
    try:
        f = Fernet(validated_key)
        token = f.encrypt(valeur.encode())
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Résultat du cryptage</title>
        </head>
        <body>
            <h2>Résultat du cryptage</h2>
            <p><strong>Valeur d'origine :</strong> {valeur}</p>
            <p><strong>Clé utilisée :</strong> {cle}</p>
            <p><strong>Valeur cryptée :</strong> {token.decode()}</p>
            <p>Gardez votre clé, vous en aurez besoin pour décrypter!</p>
            <p><a href="/decrypt">Aller au décryptage</a></p>
        </body>
        </html>
        '''
        return render_template_string(html)
    except Exception as e:
        return f"Erreur lors du cryptage: {str(e)}"

@app.route('/decrypt')
def decrypt_form():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Décryptage</title>
    </head>
    <body>
        <h2>Décryptage avec clé personnalisée</h2>
        <form action="/decrypt/custom" method="post">
            <div>
                <label for="token">Texte crypté :</label>
                <input type="text" id="token" name="token" required>
            </div>
            <div>
                <label for="cle">Votre clé personnelle :</label>
                <input type="text" id="cle" name="cle" required>
            </div>
            <button type="submit">Décrypter</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/decrypt/custom', methods=['POST'])
def decrypt_custom():
    token = request.form.get('token', '')
    cle = request.form.get('cle', '')
    
    validated_key = validate_key(cle)
    if not validated_key:
        return "Erreur: Impossible de générer une clé valide à partir de votre entrée."
    
    try:
        f = Fernet(validated_key)
        valeur_decryptee = f.decrypt(token.encode()).decode()
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Résultat du décryptage</title>
        </head>
        <body>
            <h2>Résultat du décryptage</h2>
            <p><strong>Texte crypté :</strong> {token}</p>
            <p><strong>Clé utilisée :</strong> {cle}</p>
            <p><strong>Texte décrypté :</strong> {valeur_decryptee}</p>
            <p><a href="/encrypt">Crypter un autre message</a></p>
        </body>
        </html>
        '''
        return render_template_string(html)
    except Exception as e:
        return f"Erreur lors du décryptage: {str(e)}. Vérifiez que vous utilisez la bonne clé."
                                                                                                                                                     
if __name__ == "__main__":
    app.run(debug=True)
