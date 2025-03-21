from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world(): #kaka
    return render_template('hello.html')

# Générer la clé une seule fois et la stocker
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_decryptee = f.decrypt(token_bytes)  # Decrypt le token
        return f"Valeur décryptée : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur de décryptage : {str(e)}"
                                                                                                                                                     
if __name__ == "__main__":
    app.run(debug=True)
