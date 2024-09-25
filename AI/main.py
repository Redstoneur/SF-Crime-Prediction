from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Date(BaseModel):
    """
    Modèle Pydantic représentant une date avec des attributs d'année, de mois et de jour.
    """
    annee: int
    mois: int
    jour: int
    heure: int
    minute: int
    seconde: int

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant la date.
        :return: Chaîne de caractères représentant la date.
        """
        return f"{self.annee}-{self.mois}-{self.jour} {self.heure}:{self.minute}:{self.seconde}"

    def __datetime__(self):
        """
        Retourne un objet datetime représentant la date.
        :return: Objet datetime représentant la date.
        """
        return datetime.strptime(self.__str__(), "%Y-%m-%d %H:%M:%S")

    def __dayOfWeek__(self):
        """
        Retourne le jour de la semaine.
        :return: Jour de la semaine.
        """
        return self.__datetime__().strftime("%A")

    def __isValide__(self):
        """
        Vérifie si la date est valide.
        :return: True si la date est valide, False sinon.
        """
        try:
            self.__datetime__()
            return True
        except ValueError:
            return False


class Position(BaseModel):
    """
    Modèle Pydantic représentant une position avec des attributs de latitude et de longitude.
    """
    latitude: float
    longitude: float


class Crime(BaseModel):
    """
    Modèle Pydantic représentant un crime avec des attributs de date, d'heure, de quartier, de catégorie et de description.
    """
    dates: Date
    pdDistrict: str
    adresse: str
    position: Position


class MyAPI(FastAPI):
    """
    Classe personnalisée FastAPI qui initialise les routes.
    """

    def __init__(self):
        """
        Initialise l'application FastAPI et ajoute les routes.
        """
        super().__init__(
            title="SF-Crime-Prediction-AI",
            description="API pour prédire les crimes à San Francisco",
            version="1.0.0",
            docs_url="/docs",  # URL pour Swagger UI
            redoc_url="/redoc"  # URL pour ReDoc
        )
        self.add_routes()

    def add_routes(self):
        """
        Ajoute des routes à l'application FastAPI.
        """

        @self.get("/")
        def read_root():
            """
            Point de terminaison GET qui retourne un message de bienvenue.
            """
            return {"message": "Bonjour, le monde!"}

        @self.post("/predict")
        def predict_crime(crime: Crime):
            """
            Point de terminaison POST qui prédit l'issue de l'enquête d'un crime à San Francisco.
            """

            if not crime.dates.__isValide__():
                # Retourner une erreur si la date est invalide
                raise HTTPException(status_code=400, detail="La date est invalide.")

            if crime.pdDistrict == "" or crime.adresse == "":
                # Retourner une erreur si les informations
                raise HTTPException(status_code=400,
                                    detail="Les informations sont incomplètes. Veuillez les compléter: [" +
                                           ("pdDistrict, " if crime.pdDistrict == "" else "") +
                                           ("adresse, " if crime.adresse == "" else "") +
                                           "]"
                                    )

            data: dict[str, str] = {
                "dates": crime.dates.__str__(),
                "joursDeLaSemaine": crime.dates.__dayOfWeek__(),
                "pdDistrict": crime.pdDistrict,
                "adresse": crime.adresse,
                "x": str(crime.position.latitude),
                "y": str(crime.position.longitude)
            }

            # Prédire le crime à San Francisco
            prediction = "EN COURS DE DÉVELOPPEMENT"

            # Retourner la prédiction
            return {
                "prediction": prediction,
                "data": data
            }


# Crée une instance de l'application FastAPI
app = MyAPI()

# Si le script est exécuté directement, démarre le serveur FastAPI
if __name__ == "__main__":
    # Importe uvicorn et démarre le serveur FastAPI
    import uvicorn

    # Démarre le serveur FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000)
