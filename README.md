# SF-Crime-Prediction

---

![License](https://img.shields.io/github/license/Redstoneur/SF-Crime-Prediction)
![Top Language](https://img.shields.io/github/languages/top/Redstoneur/SF-Crime-Prediction)
![Python Version](https://img.shields.io/badge/python-3.10-blue)
![Node Version](https://img.shields.io/badge/Node-18-green)
![Size](https://img.shields.io/github/repo-size/Redstoneur/SF-Crime-Prediction)
![Contributors](https://img.shields.io/github/contributors/Redstoneur/SF-Crime-Prediction)
![Last Commit](https://img.shields.io/github/last-commit/Redstoneur/SF-Crime-Prediction)
![Issues](https://img.shields.io/github/issues/Redstoneur/SF-Crime-Prediction)
![Pull Requests](https://img.shields.io/github/issues-pr/Redstoneur/SF-Crime-Prediction)

---

![Forks](https://img.shields.io/github/forks/Redstoneur/SF-Crime-Prediction)
![Stars](https://img.shields.io/github/stars/Redstoneur/SF-Crime-Prediction)
![Watchers](https://img.shields.io/github/watchers/Redstoneur/SF-Crime-Prediction)

[//]: # (---)

[//]: # ()
[//]: # (![Latest Release]&#40;https://img.shields.io/github/v/release/Redstoneur/SF-Crime-Prediction&#41;)

[//]: # (![Release Date]&#40;https://img.shields.io/github/release-date/Redstoneur/SF-Crime-Prediction&#41;)

[//]: # (![Build Status]&#40;https://img.shields.io/github/actions/workflow/status/Redstoneur/SF-Crime-Prediction/pylint.yml&#41;)

---

## Contexte de l'Analyse

Cette analyse porte sur la classification des crimes survenant dans la ville de San Francisco. Les données proviennent du système de signalement des incidents criminels du SFPD et couvrent la période du 1er janvier 2003 au 13 mai 2015. Les ensembles de données d'entraînement et de test alternent chaque semaine, avec les semaines 1, 3, 5, 7... faisant partie de l'ensemble de test et les semaines 2, 4, 6, 8 faisant partie de l'ensemble d'entraînement.

### Description des données

- **Dates** : horodatage de l'incident criminel
- **Category** : catégorie de l'incident criminel (disponible uniquement dans train.csv). C'est la variable cible à prédire.
- **Descript** : description détaillée de l'incident criminel (disponible uniquement dans train.csv)
- **DayOfWeek** : jour de la semaine
- **PdDistrict** : nom du district de police
- **Resolution** : manière dont l'incident criminel a été résolu (disponible uniquement dans train.csv)
- **Address** : adresse approximative de l'incident criminel 
- **X** : Longitude
- **Y** : Latitude

### Liens Utiles

- Site principal : [Kaggle](https://www.kaggle.com)
- Lien direct vers l'analyse : [San Francisco Crime Classification](https://www.kaggle.com/c/sf-crime)
- Accès aux données : [Données de l'analyse](https://www.kaggle.com/c/sf-crime/data)

## Description du Projet

Ce projet est une application web qui permet de prédire les crimes à San Francisco en utilisant une IA. Le projet est divisé en deux parties : le front-end développé avec Vue 3 et le back-end développé avec FastAPI et une IA pour la prédiction.

### Prérequis

- Node.js (version 18 ou supérieure)
- Python (version 3.10 ou supérieure)
- Docker (optionnel)

### Installation et Lancement du Projet

#### Sans Docker

1. **Cloner le dépôt :**

   ```sh
   git clone https://github.com/Redstoneur/sf-crime-prediction.git
   cd sf-crime-prediction
   ```

2. **Installation et Lancement du Back-end :**

   ```sh
   cd AI
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Installation et Lancement du Front-end :**

   ```sh
   cd front-ai
   npm install
   npm run dev
   ```
   
4. **Accès à l'Application :**

    - **Front-end :** voir la console pour l'adresse, généralement [http://localhost:5173](http://localhost:5173)
    - **Back-end :** [http://localhost:8000](http://localhost:8000)

#### Avec Docker

1. **Cloner le dépôt :**

   ```sh
   git clone https://github.com/Redstoneur/sf-crime-prediction.git
   cd sf-crime-prediction
   ```

2. **Lancer les services avec Docker Compose :**

   ```sh
   docker-compose up --build
   ```

3. **Accès à l'Application :**

   - **Front-end :** [http://localhost:3000](http://localhost:3000)
   - **Back-end :** [http://localhost:8000](http://localhost:8000)

### Structure du Projet

- `AI/` : Contient le code du back-end et de l'IA.
- `front-ai/` : Contient le code du front-end.
- `docker-compose.yml` : Fichier de configuration pour Docker Compose.
- `Dockerfile` : Fichiers Docker pour le front-end et le back-end.

### Licence

Ce projet est sous licence Apache 2.0. Consultez le fichier `LICENSE` pour plus d'informations.
