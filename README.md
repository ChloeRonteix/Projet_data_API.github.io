# PROJET
Personnaliser la restitution de la donnée scrapée

![alt text](https://github.com/ChloeRonteix/Projet_data_API.github.io/blob/master/schema_système.png?raw=true)

# Equipe
- Thibault Valton
- Chloé Ronteix

# Sujet
Les données du site Allociné

# Objectifs
- Scrapper les données concernant les films du site
- Créer une base de données sur les films disponibles
- Rendre accessible ces données via une page web

# Compétences développées
- Scraping web
- Création d'une BDD relationnelle et mise en ligne de cette base sur AWS
- Création d'une API et hébergement sur Heroku
- Mise en page d'une page web hébergée sur Github_pages

# API
https://fastapiallocine.herokuapp.com/docs

# Base de données
![alt text](https://github.com/ChloeRonteix/Projet_data_API.github.io/blob/master/schema_db.png?raw=true)

# Problèmes rencontrés
- Présence de doublons dans la table "people" dû au scrapping, qui s'est répercuté sur la table de jointure "films_actors"

# Poursuite du projet dans le futur
- Nettoyage des doublons fait!
- Adapter l'envoi vers la base de données pour éviter d'insérer de nouveaux doublons (ajouter une vérification d'existence au niveau des noms si provider_id inexistant)
- Après nettoyage et adaptation, scrapper plus de pages
- Réflexion autour d'un modèle de prédiction des notes des films (en fonction des acteurs, réalisateurs, genre?)
- Ajout d'une interface de recherche sur le site internet pour naviguer dans la base de données?