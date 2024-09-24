from datetime import datetime

from fastapi import FastAPI
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
        """
        return f"{self.annee}-{self.mois}-{self.jour} {self.heure}:{self.minute}:{self.seconde}"


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
            Point de terminaison POST qui prédit le crime à San Francisco en fonction des attributs de crime fournis.
            """
            data = {
                "dates": crime.dates.__str__(),
                "joursDeLaSemaine": datetime.strptime(crime.dates.__str__(), "%Y-%m-%d %H:%M:%S").strftime("%A"),
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
