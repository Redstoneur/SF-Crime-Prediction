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


class Data(BaseModel):
    Dates: str
    DayOfWeek: str
    PdDistrict: str
    Address: str
    X: float
    Y: float


class AI:
    train_file_path: str
    test_file_path: str

    df_train: pd.DataFrame
    df_test: pd.DataFrame

    encoder: OrdinalEncoder
    clf: tree.DecisionTreeClassifier
    rf_classifier: RandomForestClassifier
    knn: KNeighborsClassifier
    acctree: float
    accrf: float
    accknn: float

    def __init__(self, directory: str, train_file: str, test_file: str) -> None:
        """
        Initialise les modèles de classification.
        :param train_file: Fichier CSV contenant les données d'entraînement.
        :param test_file: Fichier CSV contenant les données de test.
        """
        self.train_file_path = os.path.join(directory, train_file)
        self.test_file_path = os.path.join(directory, test_file)

        self.df_train = pd.read_csv(self.train_file_path)
        self.df_test = pd.read_csv(self.test_file_path)

        if self.df_test is None or self.df_train is None:
            raise Exception("One of the dataframes is empty")

        # Categorize 'Resolution' into broader categories
        self.df_train['Categorie'] = ''
        self.df_train.loc[self.df_train['Resolution'].isin(
            ['ARREST, BOOKED', 'ARREST, CITED', 'JUVENILE CITED', 'JUVENILE BOOKED', 'PROSECUTED FOR LESSER OFFENSE',
             'PROSECUTED BY OUTSIDE AGENCY']), 'Categorie'] = 'Arrestation / Poursuites'
        self.df_train.loc[self.df_train['Resolution'].isin(
            ['COMPLAINANT REFUSES TO PROSECUTE', 'DISTRICT ATTORNEY REFUSES TO PROSECUTE', 'NOT PROSECUTED',
             'JUVENILE ADMONISHED', 'JUVENILE DIVERTED', 'CLEARED-CONTACT JUVENILE FOR MORE INFO', 'PSYCHOPATHIC CASE',
             'EXCEPTIONAL CLEARANCE']), 'Categorie'] = 'Absence de poursuites / Refus / Cas particuliers'
        self.df_train.loc[
            self.df_train['Resolution'].isin(
                ['LOCATED', 'UNFOUNDED']), 'Categorie'] = 'Localisation / État de la personne'
        self.df_train.loc[self.df_train['Resolution'].isin(['NONE']), 'Categorie'] = 'Indépendant (NONE)'

        df_train_patch = self.df_train[['Dates', 'Categorie', 'DayOfWeek', 'PdDistrict', 'Address', 'X', 'Y']]
        df_test_patch = self.df_test[
            ['Dates', 'DayOfWeek', 'PdDistrict', 'Address', 'X', 'Y']]  # todo : check if this is correct

        categorical_features = [col for col in df_train_patch.columns if self.df_train[col].dtype == 'object']
        self.encoder = OrdinalEncoder(cols=categorical_features).fit(df_train_patch)
        df_train_patch_2 = self.encoder.transform(df_train_patch)

        nb = 25000
        df_train_patch_sample = pd.concat([
            df_train_patch_2[df_train_patch_2.Categorie == i].sample(
                min(nb, len(df_train_patch_2[df_train_patch_2.Categorie == i])), replace=True)
            for i in range(4)
        ])

        y = df_train_patch_sample.Categorie
        X = df_train_patch_sample.drop(['Categorie'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Decision Tree
        self.clf = tree.DecisionTreeClassifier().fit(X_train, y_train)
        self.acctree = self.clf.score(X_test, y_test) * 100
        print(f'Decision Tree Accuracy: {self.acctree:.2f}%')

        # Random Forest
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
        self.accrf = accuracy_score(y_test, self.rf_classifier.predict(X_test)) * 100
        print(f'Random Forest Accuracy: {self.accrf:.2f}%')

        # K-Nearest Neighbors
        self.knn = KNeighborsClassifier(n_neighbors=2).fit(X_train, y_train)
        self.accknn = accuracy_score(y_test, self.knn.predict(X_test)) * 100
        print(f'KNN Accuracy: {self.accknn:.2f}%')

    def predict(self, data: Data):
        """
        Prédit l'issue de l'enquête d'un crime à San Francisco.
        :param new_data: Nouvelles données à prédire.
        :return: Prédiction de l'issue de l'enquête.
        """

        warnings.filterwarnings("ignore", category=FutureWarning,
                                message=".*Downcasting object dtype arrays on .fillna.*")

        new_data: dict = {
            'Dates': [data.Dates],
            'DayOfWeek': [data.DayOfWeek],
            'PdDistrict': [data.PdDistrict],
            'Address': [data.Address],
            'X': [data.X],
            'Y': [data.Y],
            "Categorie": [None]
        }

        new_df = pd.DataFrame(new_data)
        new_df_encoded = self.encoder.transform(new_df).drop(columns=['Categorie'])

        tree_prediction = self.clf.predict(new_df_encoded)
        rf_prediction = self.rf_classifier.predict(new_df_encoded)
        knn_prediction = self.knn.predict(new_df_encoded)

        predictions = [tuple(tree_prediction), tuple(rf_prediction), tuple(knn_prediction)]
        prediction_counts = Counter(predictions)
        most_common_prediction, count = prediction_counts.most_common(1)[0]

        if count == 1:
            accuracies = {'tree': self.acctree, 'rf': self.accrf, 'knn': self.accknn}
            most_accurate_model = max(accuracies, key=accuracies.get)
            final_prediction = eval(f'{most_accurate_model}_prediction')
        else:
            final_prediction = most_common_prediction

        final_prediction = int(final_prediction[0])

        prediction_mapping = {
            0: 'Arrestation / Poursuites',
            1: 'Absence de poursuites / Refus / Cas particuliers',
            2: 'Localisation / État de la personne',
            3: 'Indépendant (NONE)'
        }

        final_prediction_text = prediction_mapping.get(final_prediction, "Catégorie inconnue")

        return final_prediction_text


if __name__ == "__main__":
    ai = AI("./../DataSet", "train.csv", "test.csv")
    data = Data(Dates="2015-05-13 23:53:00", DayOfWeek="Wednesday", PdDistrict="SOUTHERN",
                Address="800 Block of BRYANT ST", X=-122.403405, Y=37.775421)
    print(ai.predict(data))
