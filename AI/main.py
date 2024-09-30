#######################################################################################################################
### Importation des modules nécessaires ###############################################################################
#######################################################################################################################

from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Class.AI import AI, Data
from Class.address import Address


#######################################################################################################################
### Modèle de données #################################################################################################
#######################################################################################################################


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
        :return: Chaîne de caractères représentant la date au format "AAAA-MM-JJ HH:MM:SS".
        """
        return f"{self.annee}-{self.mois:02d}-{self.jour:02d} {self.heure:02d}:{self.minute:02d}:{self.seconde:02d}"

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
    Modèle Pydantic représentant un crime avec des attributs de date, d'heure, de quartier,
    de catégorie et de description.
    """
    dates: Date
    pdDistrict: str
    adresse: str
    position: Position


class Crime2(BaseModel):
    """
    Modèle Pydantic représentant un crime avec des attributs de date, d'heure, de quartier,
    de catégorie et de description.
    """
    dates: Date
    pdDistrict: str
    adresse: str


#######################################################################################################################
### Classe personnalisée FastAPI ######################################################################################
#######################################################################################################################

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
        # noinspection PyTypeChecker
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Permettre toutes les origines, à ajuster selon vos besoins
            allow_credentials=True,
            allow_methods=["*"],  # Permettre toutes les méthodes HTTP
            allow_headers=["*"],  # Permettre tous les en-têtes
        )
        self.add_routes()
        print("Initialisation de l'IA...")
        self.ai = AI("./DataSet", "train.csv", "test.csv")
        print("IA initialisée.")

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

        @self.get("/address/{address}")
        def check_address(address: str):
            """
            Point de terminaison POST qui vérifie la validité d'une adresse et retourne sa latitude et sa longitude.
            """
            addr: Address = Address(address)
            return {
                "address": addr.address,
                "valid": addr.is_valid(),
                "adresse_location": addr.address_location,
                "latitude": addr.latitude,
                "longitude": addr.longitude
            }

        @self.post("/address")
        def check_address(position: Position):
            """
            Point de terminaison POST qui vérifie la validité d'une adresse et retourne sa latitude et sa longitude.
            """
            addr: Address = Address.create_address_by_position((position.latitude, position.longitude))
            return {
                "address": addr.address,
                "valid": addr.is_valid(),
                "adresse_location": addr.address_location,
                "latitude": addr.latitude,
                "longitude": addr.longitude
            }

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

            data: Data = Data(
                Dates=crime.dates.__str__(),
                DayOfWeek=crime.dates.__dayOfWeek__(),
                PdDistrict=crime.pdDistrict,
                Address=crime.adresse,
                X=crime.position.latitude,
                Y=crime.position.longitude
            )

            # Prédire le crime à San Francisco
            prediction = self.ai.predict(data)

            # Retourner la prédiction
            return {
                "prediction": prediction,
                "data": data
            }

        @self.post("/predict2")
        def predict_crime2(crime: Crime2):
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

            # Création de l'adresse
            addr = Address(crime.adresse)

            # Vérification de la validité de l'adresse
            if not addr.is_valid():
                # Retourner une erreur si l'adresse est invalide
                raise HTTPException(status_code=400, detail="L'adresse est invalide.")

            data: Data = Data(
                Dates=crime.dates.__str__(),
                DayOfWeek=crime.dates.__dayOfWeek__(),
                PdDistrict=crime.pdDistrict,
                Address=crime.adresse,
                X=crime.position.latitude,
                Y=crime.position.longitude
            )

            # Prédire le crime à San Francisco
            prediction = self.ai.predict(data)

            # Retourner la prédiction
            return {
                "prediction": prediction,
                "data": data
            }

        @self.get("/accuracy")
        def get_accuracy():
            """
            Point de terminaison GET qui retourne les précisions des modèles.
            """
            return self.ai.get_accuracy()


#######################################################################################################################
### Point d'entrée de l'application ###################################################################################
#######################################################################################################################

# Crée une instance de l'application FastAPI
app = MyAPI()

#######################################################################################################################
### Test d'utilisation ################################################################################################
#######################################################################################################################


# Si le script est exécuté directement, démarre le serveur FastAPI
if __name__ == "__main__":
    # Importe uvicorn et démarre le serveur FastAPI
    import uvicorn

    # Démarre le serveur FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000)

#######################################################################################################################
### Fin du fichier address.py #########################################################################################
#######################################################################################################################
