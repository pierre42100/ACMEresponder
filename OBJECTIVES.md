Spécifications : https://www.rfc-editor.org/rfc/rfc8555  

Objectifs clairs : Le projet est réussi si : 

* Il dispose d’une documentation dans le code source et un readme expliquant comment l'exécuter 
* Il permet d’obtenir de manière sécurisée des certificats d’une autorité de certification 
* Le code est propre (note > 8 dans pylint pour le dossier `src`) 

Planning : 

* Premier jalon : (pour le prochain cours) 
  * [x] Création du dépôt Git 
  * [x] Schéma d’architecture du projet 
  * [x] Construction de la route /directory 
  * [x] Génération des nonces (newNonce) 
  * [x] Création des comptes utilisateurs (newAccount) 

* Second jalon :  (05/04/2023) 
  * [x] Préparation d’une autorité de certification 
  * [-] Demande et vérification des challenges de type HTTP (newOrder) 
    * [x] Première émission de certificat
    * [ ] Nettoyage des anciens ordres
    * [ ] Prise en  compte des expirations
    * [ ] Rate limiting
  * [x] Émission de certificats 

* Troisième jalon : (07/04/2023) 
  * [ ] Construction d’une documentation de la mise en place (préparation de l’AC racine, politique d’émission...) 
  * [ ] Dockerisation de la solution 

* Jalons bonus 
  * [ ] Révocation des certificats (revokeCert) 
  * [ ] Gestion des comptes utilisateurs
  * [ ] Changement des clés (keyChange) 
  * [ ] Authentification à l’aide de challenges DNS 
  * [x] Prise en charge complète des nonce