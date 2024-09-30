"""
Ce module contient la classe AI pour l'entraînement et la prédiction des résultats des enquêtes
criminelles à San Francisco en utilisant divers modèles d'apprentissage automatique.
"""

####################################################################################################
### Importation des modules nécessaires ############################################################
####################################################################################################

import os
import warnings
from collections import Counter

import pandas as pd
from category_encoders import OrdinalEncoder
from pydantic import BaseModel
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


####################################################################################################
### Modèle de données ##############################################################################
####################################################################################################

class Data(BaseModel):
    """
    Modèle de données pour les données d'entrée utilisées dans les prédictions.
    """
    Dates: str
    DayOfWeek: str
    PdDistrict: str
    Address: str
    X: float
    Y: float


####################################################################################################
### Classe AI ######################################################################################
####################################################################################################

class AI:
    """
    Classe AI pour l'entraînement et la prédiction des résultats des enquêtes criminelles
    à San Francisco.
    """
    # Chemin du fichier d'entraînement
    train_file_path: str
    # Chemin du fichier de test
    test_file_path: str

    # DataFrame pour les données d'entraînement
    df_train: pd.DataFrame
    # DataFrame pour les données de test
    df_test: pd.DataFrame

    # Encodeur ordinal pour les caractéristiques catégorielles
    encoder: OrdinalEncoder
    # Classificateur d'arbre de décision
    clf: tree.DecisionTreeClassifier
    # Classificateur de forêt aléatoire
    rf_classifier: RandomForestClassifier
    # Classificateur K-Nearest Neighbors
    knn: KNeighborsClassifier
    # Précision de l'arbre de décision
    acctree: float
    # Précision de la forêt aléatoire
    accrf: float
    # Précision du K-Nearest Neighbors
    accknn: float

    # Mappage des prédictions aux catégories
    prediction_mapping: dict = {
        0: 'Arrestation ou Poursuites Judiciaires',
        1: 'Aucune Poursuite ou Refus de Poursuite',
        2: 'Personne Localisée ou Cas Non Fondé',
        3: 'Aucune Action Juridique Prise'
    }

    def __init__(self, directory: str, train_file: str, test_file: str) -> None:
        """
        Initialise la classe AI avec les données d'entraînement et de test.

        :param directory: Répertoire contenant les fichiers CSV.
        :param train_file: Fichier CSV avec les données d'entraînement.
        :param test_file: Fichier CSV avec les données de test.
        """
        self.train_file_path = os.path.join(directory, train_file)
        self.test_file_path = os.path.join(directory, test_file)

        self.load_data()
        self.categorize_data()
        self.encode_data()
        self.sample_data()
        self.train_models()

    def load_data(self):
        """
        Load training and test data from CSV files.
        """
        self.df_train = pd.read_csv(self.train_file_path)
        self.df_test = pd.read_csv(self.test_file_path)

        # Vérifier si l'un des DataFrames est vide
        if self.df_test is None or self.df_train is None:
            raise ValueError("L'un des DataFrames est vide")

    def categorize_data(self):
        """
        Catégoriser 'Resolution' en catégories plus larges.
        """
        self.df_train['Categorie'] = ''
        self.df_train.loc[self.df_train['Resolution'].isin([
            'ARREST, BOOKED', 'ARREST, CITED', 'JUVENILE CITED',
            'JUVENILE BOOKED', 'PROSECUTED FOR LESSER OFFENSE',
            'PROSECUTED BY OUTSIDE AGENCY'
        ]), 'Categorie'] = self.prediction_mapping[0]
        self.df_train.loc[self.df_train['Resolution'].isin([
            'COMPLAINANT REFUSES TO PROSECUTE', 'DISTRICT ATTORNEY REFUSES TO PROSECUTE',
            'NOT PROSECUTED', 'JUVENILE ADMONISHED', 'JUVENILE DIVERTED',
            'CLEARED-CONTACT JUVENILE FOR MORE INFO', 'PSYCHOPATHIC CASE',
            'EXCEPTIONAL CLEARANCE'
        ]), 'Categorie'] = self.prediction_mapping[1]
        self.df_train.loc[self.df_train['Resolution'].isin([
            'LOCATED', 'UNFOUNDED'
        ]), 'Categorie'] = self.prediction_mapping[2]
        self.df_train.loc[self.df_train['Resolution'].isin([
            'NONE'
        ]), 'Categorie'] = self.prediction_mapping[3]

    def encode_data(self):
        """
        Encode categorical features.
        """
        df_train_patch = self.df_train[
            ['Dates', 'Categorie', 'DayOfWeek', 'PdDistrict', 'Address', 'X', 'Y']
        ]
        categorical_features = [
            col for col in df_train_patch.columns if self.df_train[col].dtype == 'object'
        ]
        self.encoder = OrdinalEncoder(cols=categorical_features).fit(df_train_patch)
        self.df_train_patch_2 = self.encoder.transform(df_train_patch)

    def sample_data(self):
        """Sample data to balance classes."""
        nb = 25000
        self.df_train_patch_sample = pd.concat([
            self.df_train_patch_2[self.df_train_patch_2.Categorie == i].sample(
                min(nb, len(self.df_train_patch_2[self.df_train_patch_2.Categorie == i])),
                replace=True)
            for i in range(4)
        ])

    def train_models(self):
        """
        Entraîne les modèles d'arbre de décision, de forêt aléatoire et de KNN.
        """
        y = self.df_train_patch_sample.Categorie
        x = self.df_train_patch_sample.drop(['Categorie'], axis=1)
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.33, random_state=42
        )

        self.clf = tree.DecisionTreeClassifier().fit(x_train, y_train)
        self.acctree = self.clf.score(x_test, y_test) * 100
        print(f'Précision de l\'arbre de décision: {self.acctree:.2f}%')

        # noinspection PyTypeChecker
        self.rf_classifier = RandomForestClassifier(
            n_estimators=100, random_state=42
        ).fit(x_train, y_train)
        self.accrf = accuracy_score(y_test, self.rf_classifier.predict(x_test)) * 100
        print(f'Précision de la forêt aléatoire: {self.accrf:.2f}%')

        self.knn = KNeighborsClassifier(n_neighbors=2).fit(x_train, y_train)
        self.accknn = accuracy_score(y_test, self.knn.predict(x_test)) * 100
        print(f'Précision du KNN: {self.accknn:.2f}%')

    def predict(self, d: Data):
        """
        Prédit l'issue de l'enquête d'un crime à San Francisco.

        :param d: Nouvelles données à prédire.
        :return: Prédiction de l'issue de l'enquête.
        """
        warnings.filterwarnings("ignore", category=FutureWarning,
                                message=".*Downcasting object dtype arrays on .fillna.*")

        new_df_encoded = self.prepare_data(d)
        predictions = self.make_predictions(new_df_encoded)
        final_prediction = self.determine_final_prediction(predictions)

        final_prediction_text = self.prediction_mapping.get(final_prediction, "Catégorie inconnue")
        return final_prediction_text

    def prepare_data(self, d: Data) -> pd.DataFrame:
        """
        Prépare les nouvelles données pour la prédiction.

        :param d: Nouvelles données à prédire.
        :return: DataFrame encodé des nouvelles données.
        """
        new_data = {
            'Dates': [d.Dates],
            'DayOfWeek': [d.DayOfWeek],
            'PdDistrict': [d.PdDistrict],
            'Address': [d.Address],
            'X': [d.X],
            'Y': [d.Y],
            "Categorie": [None]
        }
        new_df = pd.DataFrame(new_data)
        new_df_encoded = self.encoder.transform(new_df).drop(columns=['Categorie'])
        return new_df_encoded

    def make_predictions(self, new_df_encoded: pd.DataFrame) -> list:
        """
        Fait des prédictions avec les trois modèles.

        :param new_df_encoded: DataFrame encodé des nouvelles données.
        :return: Liste des prédictions des trois modèles.
        """
        tree_prediction = self.clf.predict(new_df_encoded)
        rf_prediction = self.rf_classifier.predict(new_df_encoded)
        knn_prediction = self.knn.predict(new_df_encoded)
        return [tuple(tree_prediction), tuple(rf_prediction), tuple(knn_prediction)]

    def determine_final_prediction(self, predictions: list) -> int:
        """
        Détermine la prédiction finale en fonction des prédictions des modèles.

        :param predictions: Liste des prédictions des trois modèles.
        :return: Prédiction finale.
        """
        prediction_counts = Counter(predictions)
        most_common_prediction, count = prediction_counts.most_common(1)[0]

        if count == 1:
            model_predictions = {
                'tree': predictions[0],
                'rf': predictions[1],
                'knn': predictions[2]
            }
            accuracies = {'tree': self.acctree, 'rf': self.accrf, 'knn': self.accknn}
            most_accurate_model = max(accuracies, key=accuracies.get)
            final_prediction = model_predictions[most_accurate_model]
        else:
            final_prediction = most_common_prediction

        return int(final_prediction[0])

    def get_accuracy(self) -> dict:
        """
        Obtient la précision des modèles entraînés.

        :return: Dictionnaire contenant la précision de chaque modèle et la précision globale.
        """
        return {
            'tree': self.acctree,  # Précision de l'arbre de décision
            'rf': self.accrf,  # Précision de la forêt aléatoire
            'knn': self.accknn,  # Précision du K-Nearest Neighbors
            'global_accuracy': (
                                       self.acctree + self.accrf + self.accknn
                               ) / 3  # Précision globale moyenne
        }


####################################################################################################
### Test d'utilisation #############################################################################
####################################################################################################

# Point d'entrée principal du script
if __name__ == "__main__":
    # Crée une instance de la classe AI avec les chemins des fichiers d'entraînement et de test
    print("Initialisation de l'IA...")
    ai = AI("./../DataSet", "train.csv", "test.csv")
    print("IA initialisée avec succès!")

    print()

    # Crée un objet Data avec des valeurs d'exemple
    data = Data(Dates="2015-05-13 23:53:00", DayOfWeek="Wednesday", PdDistrict="SOUTHERN",
                Address="800 Block of BRYANT ST", X=-122.403405, Y=37.775421)

    # Prédit l'issue de l'enquête criminelle et affiche le résultat
    print(ai.predict(data))

####################################################################################################
### Fin du fichier ai.py ###########################################################################
####################################################################################################
