# Dossier DataSet

## Description

Ici se trouve les données utilisées pour l'entraînement des modèles de Machine Learning.
Il faut deux fichiers csv. Un fichier pour les données d'entraînement `train.csv` et un fichier pour les données de test
`test.csv`.

Le fichier train.csv contient les colonnes suivantes :

- Dates : date et heure de l'incident
- Category : catégorie de l'incident
- Descript : description de l'incident
- DayOfWeek : jour de la semaine
- PdDistrict : district de police
- Resolution : résolution de l'incident
- Address : adresse de l'incident
- X : longitude
- Y : latitude

Le fichier test.csv contient les colonnes suivantes :

- Id : identifiant unique de l'incident
- Dates : date et heure de l'incident
- DayOfWeek : jour de la semaine
- PdDistrict : district de police
- Address : adresse de l'incident
- X : longitude
- Y : latitude

## Source

Les données proviennent de la compétition
Kaggle [San Francisco Crime Classification](https://www.kaggle.com/c/sf-crime).