Spécifications : https://www.rfc-editor.org/rfc/rfc8555  

Objectifs clairs : Le projet est réussi si : 

* Il dispose d’une documentation dans le code source et un readme expliquant comment l'exécuter 
* Il permet d’obtenir de manière sécurisée des certificats d’une autorité de certification 
* Le code est propre (coding style) 

Planning : 

* Premier jalon : (pour le prochain cours) 
  * [x] Création du dépôt Git 
  * [ ] Schéma d’architecture du projet 
  * [ ] Construction de la route /directory 
  * [ ] Génération des nonces (newNonce) 
  * [ ] Création des comptes utilisateurs (newAccount) 

* Second jalon :  
  * [ ] Préparation d’une autorité de certification 
  * [ ] Demande et vérification des challenges de type HTTP (newOrder) 
  * [ ] Émission de certificats 

* Troisième jalon : 
  * [ ] Construction d’une documentation de la mise en place (préparation de l’AC racine, politique d’émission...) 
  * [ ] Dockerisation de la solution 

* Jalons bonus 
  * [ ] Révocation des certificats (revokeCert) 
  * [ ] Changement des clés (keyChange) 
  * [ ] Authentification à l’aide de challenges DNS 
  * [ ] Prise en charge complète des nonce