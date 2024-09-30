"""
Module permettant de vérifier la validité d'une adresse et de récupérer sa latitude et sa longitude.
"""

####################################################################################################
### Importation des modules nécessaires ############################################################
####################################################################################################

from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim


####################################################################################################
### Classe Address #################################################################################
####################################################################################################

class Address:
    """
    Classe permettant de vérifier la validité d'une adresse et de récupérer sa latitude et
    sa longitude.
    """

    def __init__(self, addr: str):
        """
        Initialise une adresse.
        :param addr: Adresse à vérifier.
        """
        self.address = addr
        self.address_location = None
        self.latitude = None
        self.longitude = None
        self.valid = False
        self.check_validity()

    def check_validity(self):
        """
        Vérifie la validité de l'adresse et récupère sa latitude et sa longitude si elle est valide.
        :return: None
        """
        try:
            geolocator = Nominatim(user_agent="geo_checker")
            location = geolocator.geocode(self.address)
            if location:
                self.address_location = location.address
                self.valid = True
                self.latitude = location.latitude
                self.longitude = location.longitude
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Erreur lors de la vérification de l'adresse : {e}")

    def __str__(self) -> str:
        """
        Retourne une chaîne de caractères représentant l'adresse.
        :return: Chaîne de caractères représentant l'adresse.
        """
        return f"Adresse valide : {self.address}" if self.valid else "Adresse invalide."

    def get_position(self) -> tuple[float, float]:
        """
        Retourne la latitude et la longitude de l'adresse.
        :return: Latitude et longitude de l'adresse.
        """
        return self.latitude, self.longitude

    def is_valid(self) -> bool:
        """
        Vérifie si l'adresse est valide.
        :return: True si l'adresse est valide, False sinon.
        """
        return self.valid

    @staticmethod
    def check_address_validity(addr: str) -> bool:
        """
        Vérifie la validité d'une adresse.
        :param addr: Adresse à vérifier.
        :return: True si l'adresse est valide, False sinon.
        """
        try:
            geolocator = Nominatim(user_agent="geo_checker")
            location = geolocator.geocode(addr)
            return bool(location)
        except (GeocoderTimedOut, GeocoderServiceError):
            return False

    @staticmethod
    def create_address_by_position(position: tuple[float, float]) -> 'Address':
        """
        Crée une adresse à partir d'une position.
        :param position: Position à convertir en adresse.
        :return: Adresse correspondant à la position.
        """
        geolocator = Nominatim(user_agent="geo_checker")
        location = geolocator.reverse(position)
        return Address(location.address)


####################################################################################################
### Test d'utilisation #############################################################################
####################################################################################################

if __name__ == "__main__":
    addresses: list[str] = [
        "1600 Amphitheatre Parkway, Mountain View, CA",
        "Quelque part dans le monde",
        "Paris, France",
        "63 rue d'Andrésy, Chanteloup-les-Vignes"
    ]
    for address in addresses:
        print(f"Vérification de l'adresse : {address}")
        adr = Address(address)
        print(adr)
        if adr.is_valid():
            print(f"Adresse_location : {adr.address_location}")
            print(f"Latitude : {adr.latitude}, Longitude : {adr.longitude}")
        print()


    address_test: Address = Address("63 rue d'Andrésy, Chanteloup-les-Vignes")
    print(f"Vérification des coordonnées de l'adresse : {address_test.address}")
    print(f"Vérification de l'adresse : {address_test.latitude}, {address_test.longitude}")
    adr = Address.create_address_by_position((address_test.latitude, address_test.longitude))

    print(adr)
    if adr.is_valid():
        print(f"Adresse_location : {adr.address_location}")
        print(f"Latitude : {adr.latitude}, Longitude : {adr.longitude}")
    print()

    if address_test.address_location == adr.address_location:
        print("Les adresses sont identiques.")
    else:
        print("Les adresses sont différentes.")


####################################################################################################
### Fin du fichier address.py ######################################################################
####################################################################################################
