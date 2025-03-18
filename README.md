# td_randsom
TD Cyber Randsom

Salt : valeur aléatoire ajoutée à un mdp ou une clef avant de le hacher (utiliser par exemple pour se proteger des attaques tables arc-en-ciel)
Hachage : transformer une empreinte en une donnée unique et irreversible.
Token : valeur unique utilisée pour l'authentification, l'autorisation ou l'identification d'un utilisateur ou d'un système.



 ----- Q1 : Quelle est le nom de l'algorithme de chiffrement ? Est-il robuste et pourquoi ?

Le nom de l'algorythme de chiffrement est un Cipher XOR : c'est un chiffrement additif (disjonction exclusif, principe du XOR)
"Pour déchiffrer la sortie, il suffit de réappliquer la fonction XOR avec la clé pour supprimer le chiffrement" Il n'est donc pas (selon moi) robuste 
- Il est facilement réversible (il suffit d'un XOR avec la clef)
C = P ⊕ K (chiffrement)
𝑃 = 𝐶 ⊕ 𝐾(dechiffrement)
(selon wikipedia)
- L'algorythme est fragile : on peut l'attaquer avec un K = P ⊕ C pour récupérer la clef, et ainsi tout déchiffrer
(selon un site sur internet)

-----  Trouver les fichiers (code) dans ransomware.py : 

Fonction get_files(self, filter:str) : #MODIF

------   Génération des secrets

Fonction do_derivation #MODIF dans la classe SecretManager
Fonction create(self) #MODIF dans la classe SecretManager

------  Q2 : Pourquoi ne pas hacher le sel et la clef directement ? Et avec un hmac  
Les raison pour lesquelles on ne hache pas le sel et la clef directement : 
  1 : La fonction SHA-256 est une fonction de hachage rapide : faible resistance aux attaques brtue (un attaquant peut facilement tester des millions de combinaisons par seconde) : aussi faible face aux tables arc-en-ciel (encore)
  2 : Un hachage direct ne modifie pas suffisamment la structure d’une clé "faible"

  HMAC; fonction :  hmac_key = HMAC(key, salt, SHA256).digest()
  HMAC (Hash-based Message Authentication Code) est une fonction cryptographique qui permet de dériver une clé ou d’assurer l’authenticité d’un message, mais ne ralentirait pas les attaques par brute-force. PBKDF2-HMAC, en revanche, applique des milliers d’itérations et améliore la sécurité de la clé dérivée.

------ Enrollemment

Fonction post_new(self, salt:bytes, key:bytes, token:bytes) dans la classe SecretManager : #MODIF

----- Setup
Fonction setup(self) dans la classe SecretManager : #MODIF

----- Q3 :  Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?
Vérifier si token.bin existe déjà permet :
 - D’éviter d’écraser un token existant et de casser le chiffrement 
 - D’assurer que le ransomware utilise toujours la même identification sur une machine infectée

----- Chiffrement des fichiers

Fonction xorfiles(self, files:List[str]) dans la classe SecretManager: #MODIF

----- Rendre le token affichablke

Fonction def get_hex_token(self) dans la classe Secret manager

----- Encrypt

Fonction def get_hex_token(self) dans la classe Ransomware
(Binaire --> Hexa (pour être lisible)

----- Charger les éléments cryptographiques

Fonction load(self) dans la classe Secret Manager
Celui la est cool il charge les données cryptographiés (sympa)

----- Verifier et utiliser la clef
-- Q4 
Pour vérifier que la clé fournie est correcte on utilise la fonction do_derivation pour dériver un token à parti du self, et de la key. Ensuite, on compare : si le token calculé correspond au token stocké, la clé est alors correct. 

#On implémente ces fonctions pour tester la clé
Fonction check_key(self, candidate_key:bytes) #MODIF dans la classe SecretManager
Fonction set_key(self, b64_key:str) #MODIF dans la classe SecretManager

----- Mr Propre 

Fonction clean(self) #MODIF dans la classe SecretManager
#On supprimes les dossiers contenants la clé

----- Decrypt

Fonction decrypt(self) #MODIF dans la classe Ransomware

Et c'est finis plus qu'a RUN
    
