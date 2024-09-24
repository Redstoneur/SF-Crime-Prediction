from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    """
    Modèle Pydantic représentant un utilisateur avec un attribut nom.
    """
    name: str


class MyAPI(FastAPI):
    """
    Classe personnalisée FastAPI qui initialise les routes.
    """

    def __init__(self):
        """
        Initialise l'application FastAPI et ajoute les routes.
        """
        super().__init__()
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

        @self.get("/hello/{name}")
        def say_hello(name: str):
            """
            Point de terminaison GET qui retourne un message de salutation personnalisé.

            Args:
                name (str): Le nom de la personne à saluer.

            Returns:
                dict: Un dictionnaire contenant le message de salutation.
            """
            return {"message": f"Bonjour, {name}!"}

        @self.post("/welcome")
        def welcome_user(user: User):
            """
            Point de terminaison POST qui souhaite la bienvenue à un utilisateur.

            Args:
                user (User): Un objet User contenant le nom de l'utilisateur.

            Returns:
                dict: Un dictionnaire contenant le message de bienvenue.
            """
            return {"message": f"Bienvenue, {user.name}!"}

# Crée une instance de l'application FastAPI
app = MyAPI()

# Si le script est exécuté directement, démarre le serveur FastAPI
if __name__ == "__main__":
    # Importe uvicorn et démarre le serveur FastAPI
    import uvicorn

    # Démarre le serveur FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000)
